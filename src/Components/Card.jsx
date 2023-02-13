//import { Button } from '@carbon/react'
import axios from 'axios'
import './card.scss'
import { useState, useEffect, useContext } from 'react'
import { Tag } from '@carbon/react'

const CARD_IMG_URL = "http://www.redhat.com/architect/portfolio/repo/images/"

import { FilterContext } from '@/App.jsx'

export default function Card() {

  const { filterTagList } = useContext(FilterContext)
  const [isLoading, setIsLoading] = useState(true)
  const [result, setResult] = useState([])
  const [filteredResult, setFilteredResult] = useState([])

  useEffect(() => {
    axios.get('pa/0').then((res) => {
      setResult(res.data)
      setIsLoading(false)
    })
      .catch((err) => {
        console.log(err)
      })
  }, [])

  useEffect(() => {
    if (filterTagList.length > 0) {
      console.log(filterTagList)
      var results = []
      for (const tag of filterTagList) {
        for (const item of result) {
          if (item.ProductType.includes(tag) || item.Solutions.includes(tag) || item.Vertical.includes(tag) || item.Product.includes(tag)) {
            results.push(item)
          }
        }
      }
      setFilteredResult(results)
    }
  }, [filterTagList])

  if (isLoading) {
    return <div>Loading...</div>
  }

  return (
    <>
      {
        filterTagList.length > 0 ? cardList({ list: filteredResult }) : cardList({ list: result })
      }
    </>
  )
}

function cardList({ list }) {
  return (list.map((item, _) =>
    <div className='card'>
      <img src={CARD_IMG_URL + item.Image1Url} className='cardImage' />
      <h4 className='cardHeader'>{item.Heading}</h4>
      <div className='cardContent'>{item.Summary}</div>

      {
        item.ProductType.split(",").map(typetag =>
          <Tag type="red" title="Clear Filter" key={item.ppid + typetag}></Tag>
        )}
      {
        item.Solutions.split(",").map(solutiontag =>
          <Tag type="magenta" title="Clear Filter" key={item.ppid + solutiontag}>{solutiontag}</Tag>
        )}
      {
        item.Vertical.split(",").map(verticaltag =>
          <Tag type="warm-gray" title="Clear Filter" key={item.ppid + verticaltag} >{verticaltag}</Tag>
        )}
      {
        item.Product.split(",").map(producttag =>
          <Tag type="cool-gray" title="Clear Filter" key={item.ppid + producttag}>{producttag}</Tag>
        )}

    </div>
  ))
}