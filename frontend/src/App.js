import MainPage from "./pages/mainPage";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import Login from "./pages/authorization/logIn";
import Register from "./pages/authorization/signUp";
import BookDetailPage from "./pages/BookDetailPage";


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login/>} />
        <Route path="/register" element={<Register/>} />
        <Route path="/books" element={<MainPage/>} />
        <Route path="/books/:id" element={<BookDetailPage />} />
      </Routes>
    </Router>
  );
}

export default App;
