import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import SignIn from "./components/auth/SignIn/SignIn";
import SignUp from "./components/auth/SignUp/SignUp";

function App() {
  return (
    <Router>
      <Routes>
        {/* <Route path="/" element={<Feed />} /> */}
        <Route path="/sign-in" element={<SignIn />} />
        <Route path="/sign-up" element={<SignUp />} />
        {/* Optional: Redirect unknown paths to home */}
        {/* <Route path="*" element={<Navigate to="/" />} /> */}
      </Routes>
    </Router>
  );
}

export default App;
