import { User } from './user.model';

export class Post {
  uuid: string;
  title: string;
  content: string;
  created_at: string;
  updated_at: string;
  author: User;
  votes: number;
  comments: number;
  user_vote: any;
  user_bookmark: any;
}
