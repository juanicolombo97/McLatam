import { Link } from 'react-router-dom'
const MenuBar = () => {
  return (
    <nav className="d-flex justify-content-center">
      <div className="p-2">
        <Link to="/dashboard">Expedientes</Link>
      </div>
    </nav>
  )
}
export default MenuBar