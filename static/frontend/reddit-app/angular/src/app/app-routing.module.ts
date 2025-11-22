import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { FeedComponent } from './feed/feed.component';
import { SignInComponent } from './auth/sign-in/sign-in.component';
import { SignUpComponent } from './auth/sign-up/sign-up.component';
import { SignOutComponent } from './auth/sign-out/sign-out.component';
import { AuthGuard } from './core/guards/auth/auth.guard';

import { CreatePostComponent } from './post/create-post/create-post.component';
import { PostDetailComponent } from './post/post-detail/post-detail.component';

import { SearchComponent } from './search/search.component';

import { ProfileComponent } from './profiles/profiles/profiles.component';
import { GroupComponent } from './group/group/group.component';
import { GroupRouterComponent } from './group/group-router/group-router.component';
import { GroupPostComponent } from './group/group-post/group-post.component';
import { CreateGroupComponent } from './group/create-group/create-group.component';
import { GroupSearchComponent } from './group/group-search/group-search.component';

const routes: Routes = [
  {
    path: '',
    component: FeedComponent,
  },
  {
    path: 'search',
    component: SearchComponent
  },
  {
    path: 'create',
    component: CreatePostComponent
  },
  {
    path: 'sign-in',
    component: SignInComponent,
  },
  {
    path: 'sign-up',
    component: SignUpComponent,
  },
  {
    path: 'logout',
    component: SignOutComponent
  },
  {
    path: 'all_groups',
    component: GroupSearchComponent
  },
  {
    path: 'user/:username',
    component: ProfileComponent,
  },
  {
    path: 'group',
    component: GroupRouterComponent,
    children: [
      {
        path: 'create-new',
        canActivate: [AuthGuard],
        component: CreateGroupComponent
      },
      {
        path: ':id',
        children: [
          {
            path: '',
            component: GroupComponent,
          },
          {
            path: 'submit-post',
            canActivate: [AuthGuard],
            component: GroupPostComponent
          }
        ]
      },
      {
        path: '**',
        redirectTo: '',
        pathMatch: 'full'
      }
    ]
  },
  {
    path: ':uuid',
    component: PostDetailComponent
  },
  {
    path: '**',
    redirectTo: ''
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
