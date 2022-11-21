export class TagType {
  id: number;
  title: string;
}

export class Tag {
  id: number;
  name: string;
  tag_type: TagType;
}
