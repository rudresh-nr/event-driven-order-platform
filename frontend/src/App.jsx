import CreateOrderPage from "./pages/CreateOrderPage";
import OrderList from "./components/OrderList";
import './App.css'

function App() {
  return (
    <div>
      <h1>Event Driven Order Platform</h1>
      <CreateOrderPage />
      <hr />
      <OrderList />
    </div>
  );
}

export default App;