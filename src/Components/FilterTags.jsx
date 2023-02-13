import { Tag } from '@carbon/react'

export default function FilterTags(props) {
  return (
    <>
      {props.tags.map(tag =>
        <Tag type="red" title="Clear Filter" key={props.ppid + tag}>{tag}</Tag>
      )}
    </>
  )
}