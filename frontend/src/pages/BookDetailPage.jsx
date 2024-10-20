import React, {useEffect, useState} from "react";
import {useLocation} from "react-router-dom";
import Layout from "../components/Layout";
import axios from "axios";

import "../styles/pages/BookDetailPage.css"
import BorrowBtn from "../components/BorrowBtn";
import OrderBtn from "../components/OrderBtn";


const BookDetailPage = (props) => {
    const API_URL = "http://localhost:8000/api"

    const [data, setData] = useState({})
    const [error, setError] = useState(null)
    const state = useLocation()
    const path = state.state.state

    useEffect(() => {
        const bookDetail = async () => {
            try{
                const response = await axios.get(`${API_URL}/library/books/${path.id}/`)
                setData(response.data)
            }
            catch (error){
                setError("Something went wrong")
            }
        }
        bookDetail()
    }, []);

    console.log(data)
    const image_src = data.image
    console.log(image_src)
    return (
        <Layout>
            <div className="book_detail_page">
                <article className="book_detail_image">
                    <div className="image_box">
                        <img src={data.image} width="400px"/>
                    </div>
                </article>
                <article className="book_detail_content">
                    <p className="book_title">{data.title}</p>
                    <p className="book_authors">{data.authors}</p>
                    <p>{data.cover}</p>
                    <div className="book_content">
                        <p><span>Daily fee: </span>{data.daily_fee}</p>
                        <p><span>Inventory: </span>{data.inventory}</p>
                    </div>
                    <div className="book_btns">
                        <BorrowBtn>Borrow</BorrowBtn>
                        <OrderBtn>Order</OrderBtn>
                    </div>
                </article>
            </div>
        </Layout>
    )
}

export default BookDetailPage
