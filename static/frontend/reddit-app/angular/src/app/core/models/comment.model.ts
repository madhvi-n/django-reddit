import { CommentService } from '@reddit/core/services/comment/comment.service';
import { User } from '@reddit/core/models/user.model';


export class Comment {
  id: number;
  user: User;
  mentioned_users: Array<User>;
  comment: string;
  votes: number;
  edited: boolean;
  is_removed: boolean;
  flair: string;
  created_at: string;
  updated_at: string;
  parent: number;
  child_count: number;
  user_vote: {
    id: number;
    user: number;
    vote: number;
  }
}

export class UserComment {
  id: number;
  comment: string;
  created_at: string;
}
