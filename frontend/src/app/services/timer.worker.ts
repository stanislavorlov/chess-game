/// <reference lib="webworker" />

let intervalId: ReturnType<typeof setInterval> | undefined;

export class Options {
  interval: number;
  command: string;
}

interface TimerMessage {
  command: 'start' | 'stop';
  interval?: number;
}

addEventListener('message', (event: MessageEvent<TimerMessage>) => {
  let { command, interval } = event.data;
  
  if (command == 'start') {
    interval = interval || 1000;
    let counter = 0;

    intervalId = setInterval(() => {
      postMessage({ time: ++counter });
    }, interval);
  }

  if (command == 'stop') {
    if (intervalId !== undefined) {
      clearInterval(intervalId);
      intervalId = undefined;
    }
  }

});
