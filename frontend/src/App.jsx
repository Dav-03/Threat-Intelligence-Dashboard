import { Routes, Route, Navigate } from 'react-router-dom'
import Login from './Login.jsx'
import Dashboard from './Dashboard.jsx'

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  )
}

export default App
