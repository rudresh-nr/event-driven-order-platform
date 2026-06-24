import CreateOrderPage from "./pages/CreateOrderPage";
import OrderList from "./components/OrderList";
import Dashboard from "./components/Dashboard";
import './App.css'

function App() {
  return (
    <div>
      <h1>Event Driven Order Platform</h1>
      <Dashboard/>
      <CreateOrderPage />
      <hr />
      <OrderList />
    </div>
  );
}

export default App;