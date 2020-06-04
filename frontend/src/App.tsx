import React from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Navigation from "./Navigation";
import WelcomeContent from "./Welcome";
import Search from "./Search/Search";
import TaxCalculator from "./TaxCalculator/TaxCalculator";
import TownsOverview from "./Search/TownsOverview";
import AccomodationsOverview from "./Search/AccomodationsOverview";
import { Route, Switch } from "react-router-dom";
import Container from "react-bootstrap/Container";
// eslint-disable-next-line
import $ from 'jquery';
// eslint-disable-next-line
import Popper from 'popper.js';
import 'bootstrap/dist/js/bootstrap.bundle.min';


class App extends React.Component {
  render() {
    return (
      <div>
        <Navigation />
        <Container className="mb-5" fluid>
        <Switch>
          <Route exact path="/" component={WelcomeContent} />
          <Route exact path="/search" component={Search} />
          <Route path="/search/towns" component={TownsOverview} />
          <Route path="/search/accomodations" component={AccomodationsOverview} />
          <Route path="/taxes" component={TaxCalculator} />
        </Switch>
        </Container>
      </div>
    );
  }
}

export default App;
