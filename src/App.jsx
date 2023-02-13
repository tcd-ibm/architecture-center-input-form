import { useState, useEffect } from 'react'
import React from 'react'
import './App.scss'
import SearchBar from './Components/SearchBar'
import AsciidocEditor from './Components/AsciidocEditor'
import Card from './Components/Card'
import { Button, Tag, Accordion, AccordionItem, Checkbox } from '@carbon/react'
import axios from 'axios'

export const FilterContext = React.createContext()

function App() {

  const [isEditorOn, SetIsEditorOn] = useState(false)
  const [filterTagList, setFilterTagList] = useState([])
  const [isLoading, setIsLoading] = useState(true)

  const [productTags, setProductTags] = useState([])
  const getProductTags = async () => {
    const res = await axios.get('product')
    setProductTags(res.data)
  }

  const [solutionTags, setSolutionTags] = useState([])
  const getSolutionTags = async () => {
    const res = await axios.get('solution')
    setSolutionTags(res.data)
  }

  const [verticalTags, setVerticalTags] = useState([])
  const getVerticalTags = async () => {
    const res = await axios.get('vertical')
    setVerticalTags(res.data)
  }

  const [typeTags, setTypeTags] = useState([])
  const getTypeTags = async () => {
    const res = await axios.get('type')
    setTypeTags(res.data)
  }

  const handlerFilterChange = (event) => {
    const { checked, id } = event.target
    if (checked) {
      console.log(filterTagList)
      setFilterTagList([...filterTagList, id])
    } else {
      setFilterTagList(filterTagList.filter((item) => item !== id))
    }

  }
  useEffect(() => {
    Promise.all([getProductTags(), getSolutionTags(), getVerticalTags(), getTypeTags()]).then(() => {
      setIsLoading(false)
    })
  }, [])

  if (isLoading) {
    return <div>Loading...</div>
  }

  const editor = isEditorOn ? <AsciidocEditor /> : null

  return (
    <>
      <FilterContext.Provider value={{ filterTagList, setFilterTagList }}>
        <div id="bodyContainer">
          {editor}
          <div id="sidebarContainer">
            <div class="fixed_elements">
              <SearchBar />
              <Button onClick={() => SetIsEditorOn(() => !isEditorOn)}>Editor</Button>
              <Accordion>

                <AccordionItem title="Solution">
                  <fieldset className="cds--fieldset">
                    {solutionTags.map((item, _) => <Checkbox labelText={item.sname} id={item.sid} checked={filterTagList.includes(item.sid)} onChange={handlerFilterChange} />)}
                  </fieldset>
                </AccordionItem>

                <AccordionItem title="Vertical">
                  <fieldset className="cds--fieldset">
                    {verticalTags.map((item, _) => <Checkbox labelText={item.vname} id={item.vid} checked={filterTagList.includes(item.vid)} onChange={handlerFilterChange} />)}
                  </fieldset>
                </AccordionItem>

                <AccordionItem title="Product">
                  <fieldset className="cds--fieldset">
                    {productTags.map((item, _) => <Checkbox labelText={item.pname} id={item.pid} checked={filterTagList.includes(item.pid)} onChange={handlerFilterChange} />)}
                  </fieldset>
                </AccordionItem>

                <AccordionItem title="Type">
                  <fieldset className="cds--fieldset">
                    {typeTags.map((item, _) => <Checkbox labelText={item.typename} id={item.tid} checked={filterTagList.includes(item.tid)} onChange={handlerFilterChange} />)}
                  </fieldset>
                </AccordionItem>

              </Accordion>
            </div>
          </div>

          <div /* separator */ />

          <div id="cardContainer">
            <Card />
          </div>

        </div>
      </FilterContext.Provider>
    </>
  )
}

export default App
