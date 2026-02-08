import { Routes } from '@angular/router';
import { PlayComponent } from './play/play.component';

export const PlayComponentRoutes: Routes = [
    {
        path: '',
        component: PlayComponent
    },
    {
        path: ':id',
        component: PlayComponent
    }
]