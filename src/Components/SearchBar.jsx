import { Search } from '@carbon/react'

export default function SearchBar() {
  return (
    <div className="sidebar">
      <Search className="searchBar"
        labelText="Search"
        placeHolderText="Search"
      />
    </div>
  )
}