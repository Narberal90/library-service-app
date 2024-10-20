import React, {useEffect, useState} from "react";
import { useNavigate } from "react-router-dom";
import { verifyToken } from "../apiService";
import axios from "axios";
import Layout from "../components/Layout";

import '../styles/pages/MainPage.css'
import FilterSort from "../components/FilterSort";

const MainPage = () => {
    const API_URL = "http://localhost:8000/api"

    const [books, setBooks] = useState([])
    const [loading, setLoading] = useState("")
    const [error, setError] = useState(null)
    const navigate = useNavigate()

    useEffect(() => {
        const checkAuth = async () => {
            try {
                await verifyToken()
            }
            catch (error) {
                navigate("/login")
            }
        }
        checkAuth()
    }, [navigate])
    useEffect(() => {
        const getBooks = async () => {
            try{
                 const response = await axios.get(`${API_URL}/library/books/`)
                setBooks(response.data)
            }
            catch{
                setError("Error with loading data")
            }
            finally{
                setLoading(false)
            }
        }
        getBooks()
    }, []);

    if (loading){
        return <h1>Loading ...</h1>
    }
    if (error){
        navigate("/login")
    }
    return (
        <Layout>
            <FilterSort />
            <ul className="list_of_books">
                {books.map(book => (
                    <li className="book_item" key={book.id}>{book.title}</li>
                ))}
            </ul>
        </Layout>
    )
}

export default MainPage
