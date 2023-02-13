//import { Button } from '@carbon/react'
import axios from 'axios'
import './card.scss'
import { useState, useEffect } from 'react'
import { Tag } from '@carbon/react'

const CARD_IMG_URL = "http://www.redhat.com/architect/portfolio/repo/images/"

export default function Card() {

  const [isLoading, setIsLoading] = useState(true)
  const [result, setResult] = useState([])

  useEffect(() => {
    axios.get('pa/0').then((res) => {
      setResult(res.data)
      setIsLoading(false)
    })
      .catch((err) => {
        console.log(err)
      })
  }, [])

  if (isLoading) {
    return <div>Loading...</div>
  }

  return (
    <>
      {result.map((item, _) =>
      (
        item.islive ?
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
          : null
      )
      )
      }
    </>
  )
}