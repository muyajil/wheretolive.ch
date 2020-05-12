import React from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Navigation from "./Navigation";
import WelcomeContent from "./ContentComponents/WelcomeContent";
import TaxCalculator from "./ContentComponents/TaxCalculator";
import { Route, Switch } from "react-router-dom";


class App extends React.Component {
  render() {
    return (
      <div>
        <Navigation />
        <Switch>
          <Route exact path="/" component={WelcomeContent} />
          <Route path="/taxes" component={TaxCalculator} />
        </Switch>
      </div>
    );
  }
}

export default App;
