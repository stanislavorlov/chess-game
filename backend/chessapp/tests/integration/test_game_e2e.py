import pytest
import asyncio
import os
import json
from playwright.async_api import async_playwright, expect
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from chessapp.infrastructure.config.config import Settings
from chessapp.infrastructure.models import GameDocument, GameHistoryDocument

# Configuration
FRONTEND_URL = "http://localhost:4200"
TEST_GAME_NAME = "E2E-Integration-Test-Game"
ARTIFACTS_DIR = "/Users/stanislavorlov/PycharmProjects/chess-game/backend/chessapp/tests/integration/artifacts"

@pytest.fixture(scope="module", autouse=True)
async def db_cleanup():
    """Cleanup test games before and after the test suite."""
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    
    # Load .env explicitly for testing context
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "chessapp", ".env"))
    
    settings = Settings()
    client = AsyncIOMotorClient(settings.MONGO_HOST)
    db = client.get_database(settings.MONGO_DB)
    
    async def _cleanup():
        await init_beanie(database=db, document_models=[GameDocument, GameHistoryDocument])
        test_games = await GameDocument.find(GameDocument.game_name == TEST_GAME_NAME).to_list()
        for game in test_games:
            await game.delete()
        print(f"Cleaned up {len(test_games)} test games.")

    await _cleanup()
    yield
    await _cleanup()
    client.close()

async def debug_failure(page, name):
    screenshot_path = os.path.join(ARTIFACTS_DIR, f"{name}.png")
    await page.screenshot(path=screenshot_path)
    print(f"FAILURE DEBUG: Screenshot saved to {screenshot_path}")
    
    try:
        player_top_html = await page.get_by_test_id("player-top").evaluate("node => node.outerHTML")
        player_bottom_html = await page.get_by_test_id("player-bottom").evaluate("node => node.outerHTML")
        print(f"FAILURE DEBUG: player-top HTML: {player_top_html}")
        print(f"FAILURE DEBUG: player-bottom HTML: {player_bottom_html}")
    except:
        print("FAILURE DEBUG: Could not dump player HTML")

async def setup_game(page, test_name):
    print(f"Navigating to {FRONTEND_URL}/play")
    await page.goto(f"{FRONTEND_URL}/play")
    await page.wait_for_selector('input[matinput]')
    
    print(f"Configuring game: {test_name}")
    await page.fill('input[matinput]', test_name)
    
    # Scroll to format selector
    format_selector = page.locator('mat-select')
    await format_selector.scroll_into_view_if_needed()
    await format_selector.click()
    
    # Select "Bullet" to get 1m option
    bullet_option = page.locator('mat-option:has-text("Bullet")')
    await bullet_option.click()
    
    # Click "1 m" (exact match)
    one_min_button = page.get_by_role("button", name="1 m", exact=True)
    await one_min_button.scroll_into_view_if_needed()
    await one_min_button.click()
    
    # Click "Play"
    play_button = page.get_by_role("button", name="Play")
    await play_button.click()
    
    # Wait for navigation to /play/:id
    await page.wait_for_url("**/play/*", timeout=15000)
    print(f"Navigated to: {page.url}")
    return page.url.split("/")[-1]

@pytest.mark.asyncio
async def test_fools_mate_e2e():
    async with async_playwright() as p:
        # observe real moves
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        # Capture console logs from browser
        page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))
        
        try:
            await setup_game(page, TEST_GAME_NAME)
            
            # Wait for board to be interactive
            await page.wait_for_selector('[data-testid="f2"]', timeout=10000)
            await asyncio.sleep(1) # Settle
            
            # Move 1: White f2-f3
            print("White moving f2-f3")
            await page.click('[data-testid="f2"]', delay=100)
            await page.click('[data-testid="f3"]', delay=100)
            
            # Wait for transition to Black
            await expect(page.locator('.player-indicator.active')).to_contain_text("Black", timeout=10000)
            await asyncio.sleep(1)
            
            # Move 1: Black e7-e5
            print("Black moving e7-e5")
            await page.click('[data-testid="e7"]', delay=100)
            await page.click('[data-testid="e5"]', delay=100)
            
            # Wait for transition to White
            await expect(page.locator('.player-indicator.active')).to_contain_text("White", timeout=10000)
            await asyncio.sleep(1)
            
            # Move 2: White g2-g4
            print("White moving g2-g4")
            await page.click('[data-testid="g2"]', delay=100)
            await page.click('[data-testid="g4"]', delay=100)
            
            # Wait for transition to Black
            await expect(page.locator('.player-indicator.active')).to_contain_text("Black", timeout=10000)
            await asyncio.sleep(1)
            
            # Move 2: Black d8-h4 (Checkmate)
            print("Black moving d8-h4 (Checkmate)")
            await page.click('[data-testid="d8"]', delay=100)
            await page.click('[data-testid="h4"]', delay=100)
            
            # Verification
            await page.wait_for_selector('li.history-item:has-text("h4")', timeout=10000)
            history = page.locator('li.history-item')
            await expect(history).to_have_count(4)
            
            print("Integration Test Successful: Fool's Mate executed.")
        except Exception as e:
            await debug_failure(page, "test_failure_fools_mate")
            raise e
        finally:
            await browser.close()

@pytest.mark.asyncio
async def test_piece_capture_e2e():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        captured_events = []
        def handle_console(msg):
            print(f"BROWSER CONSOLE: {msg.text}")
            if "Processing event: piece-captured" in msg.text:
                captured_events.append(msg.text)

        page.on("console", handle_console)
        
        try:
            await setup_game(page, TEST_GAME_NAME)
            
            # Move 1: White e2-e4
            print("White moving e2-e4")
            await page.wait_for_selector('[data-testid="e2"]')
            await page.click('[data-testid="e2"]', delay=100)
            await page.click('[data-testid="e4"]', delay=100)
            
            # Wait for transition to Black
            await expect(page.locator('.player-indicator.active')).to_contain_text("Black", timeout=10000)
            await asyncio.sleep(1)
            
            # Move 1: Black d7-d5
            print("Black moving d7-d5")
            await page.click('[data-testid="d7"]', delay=100)
            await page.click('[data-testid="d5"]', delay=100)
            
            # Wait for transition to White
            await expect(page.locator('.player-indicator.active')).to_contain_text("White", timeout=10000)
            await asyncio.sleep(1)
            
            # Move 2: White captures pawn at d5 (e4xd5)
            print("White captures d5 from e4")
            await page.click('[data-testid="e4"]', delay=100)
            await page.click('[data-testid="d5"]', delay=100)
            
            # Wait for transition to Black
            await expect(page.locator('.player-indicator.active')).to_contain_text("Black", timeout=10000)
            
            # VERIFY WEB SOCKET EVENT
            print("Verifying WebSocket piece-captured event...")
            # We wait a bit for the async console log to be captured
            timeout = 5
            while timeout > 0 and not captured_events:
                await asyncio.sleep(1)
                timeout -= 1
            
            assert len(captured_events) > 0, "No 'piece-captured' event was processed by the frontend console."
            print(f"SUCCESS: Received 'piece-captured' event: {captured_events[0]}")
            
            # Verify history contains capture notation (if implemented) or just entry count
            await page.wait_for_selector('li.history-item', timeout=5000)
            history = page.locator('li.history-item')
            await expect(history).to_have_count(3)
            
            print("Integration Test Successful: Piece capture verified via WebSocket.")
        except Exception as e:
            await debug_failure(page, "test_failure_capture")
            raise e
        finally:
            await browser.close()
