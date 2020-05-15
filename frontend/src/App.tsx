import React from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Navigation from "./Navigation";
import WelcomeContent from "./Welcome";
import Search from "./Search/Search";
import TaxCalculator from "./TaxCalculator/TaxCalculator";
import { Route, Switch } from "react-router-dom";
import Container from "react-bootstrap/Container";


class App extends React.Component {
  render() {
    return (
      <div>
        <Navigation />
        <Container fluid>
        <Switch>
          <Route exact path="/" component={WelcomeContent} />
          <Route path="/search" component={Search} />
          <Route path="/taxes" component={TaxCalculator} />
        </Switch>
        </Container>
      </div>
    );
  }
}

export default App;
