import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './pages/Home';
import Signup from './pages/Signup';
import Login from './pages/Login';
import Products from './pages/Products';
import Orders from './pages/Orders';

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/signup" component={Signup} />
          <Route path="/login" component={Login} />
          <Route path="/products" component={Products} />
          <Route path="/orders" component={Orders} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
