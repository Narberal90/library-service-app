import MainPage from "./pages/mainPage";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import Login from "./pages/authorization/logIn";
import Register from "./pages/authorization/signUp";


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login/>} />
        <Route path="/register" element={<Register/>} />
        <Route path="/" element={<MainPage/>} />
      </Routes>
    </Router>
  );
}

export default App;
