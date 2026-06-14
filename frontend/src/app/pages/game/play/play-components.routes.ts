import { Routes } from '@angular/router';
import { PlayComponent } from './play/play.component';
import { ReplayComponent } from './replay/replay.component';

export const PlayComponentRoutes: Routes = [
    {
        path: '',
        component: PlayComponent
    },
    {
        path: 'replay/:id',
        component: ReplayComponent
    },
    {
        path: ':id',
        component: PlayComponent
    }
]