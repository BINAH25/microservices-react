import React, { SyntheticEvent, useState } from 'react'
import Wrapper from './Wrapper'
import { Navigate } from 'react-router-dom'
import { REACT_APP_ADMIN_ENDPOINT } from "../constant";

const ProductsCreate = () => {
  const [title, setTitle] = useState('')
  const [image, setImage] = useState('')
  const [redirect, setRedirect] = useState(false)

  const submit = async (e: SyntheticEvent) => {
    e.preventDefault()

    await fetch(REACT_APP_ADMIN_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title,
        image,
      }),
    })

    setRedirect(true)
  }

  if (redirect) {
    return <Navigate to={'/admin/products'} />
  }

  return (
    <Wrapper>
      <form onSubmit={submit}>
        <div className='form-group'>
          <label>Title</label>
          <input
            type='text'
            className='form-control'
            name='title'
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>
        <div className='form-group'>
          <label>Image</label>
          <input
            type='text'
            className='form-control'
            name='image'
            onChange={(e) => setImage(e.target.value)}
          />
        </div>
        <button className='btn btn-outline-secondary'>Save</button>
      </form>
    </Wrapper>
  )
}

export default ProductsCreate
