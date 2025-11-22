import { User } from './user.model';
import { Group } from './group.model';
import { Tag } from './tag.model';
import { Report } from './report.model';

export class Post {
  uuid: string;
  title: string;
  content: string;
  status: string;
  created_at: string;
  updated_at: string;
  author: User;
  votes: number;
  comments: number;
  user_vote: any;
  user_bookmark: any;
  tags: Tag[];
  group: Group;
  report?: Report
}
