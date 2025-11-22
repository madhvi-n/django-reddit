import { Tag } from './tag.model';

export class Rule {
  title: string;
  description: string;
  id: number;
  group: number;
  rule_type: string;
}

export class Group {
  id: number;
  name: string;
  description: string;
  group_type: string;
  archive_posts: boolean;
  topics?: Tag[];
  rules?: Rule[];
  created_at: string;
  updated_at?: string;
  members_count?: number;
  member_status?: any;
}
