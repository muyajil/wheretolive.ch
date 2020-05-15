import React from "react";
import Container from "react-bootstrap/Container";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Card from "react-bootstrap/Card";
import Badge from "react-bootstrap/Badge";
import Button from "react-bootstrap/Button";
import { LinkContainer } from "react-router-bootstrap";
import Banner from "./Utilities/Banner";

class WelcomeContent extends React.Component {
  render() {
    return (
      <Container fluid>
        <Banner />
        <Row>
          <Col className="text-center mt-5 text-light">
            {/* <h1>#TODO Here we want to show the first page of the search form, compare to immoscout, as on overlay</h1> */}
          </Col>
        </Row>
        <Row className="mt-0 mt-lg-5">
          {/* TODO: these cards should collapse into a carousel, maybe conditional rendering?*/}
          <Col className="mt-5 mt-lg-0" xs={12} lg={3}>
            <Card className="h-100">
              <Card.Body>
                <Card.Title>
                  Commute based town search{" "}
                  <Badge variant="secondary">Exclusive</Badge>
                </Card.Title>
                <Card.Text>
                  Find out which towns are within a defined commute time using
                  public transport from your workplace. Choose whether to only
                  consider time spent in the train, i.e. for example if you
                  generally use your bike to get to the station, or whether to
                  include the time needed to get to the next train station.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          <Col className="mt-5 mt-lg-0" xs={12} lg={3}>
            <Card className="h-100">
              <Card.Body>
                <Card.Title>AI Powered Tax Estimator</Card.Title>
                <Card.Text>
                  Our tax estimator takes into account the minimum amount of
                  information needed to produce an accurate estimation of the
                  tax burden based on your gross income. The only information
                  needed is whether you are married and if you are double
                  earners and how many children are supported.
                </Card.Text>
                <LinkContainer to="/taxes">
                  <Button variant="secondary">Try it out!</Button>
                </LinkContainer>
              </Card.Body>
            </Card>
          </Col>
          <Col className="mt-5 mt-lg-0" xs={12} lg={3}>
            <Card className="h-100">
              <Card.Body>
                <Card.Title>Sophisticated Cost Analysis</Card.Title>
                <Card.Text>
                  In switzerland there are 3 main drivers that determine cost of
                  living:
                  <ul>
                    <li>Cost of accomodation</li>
                    <li>Cost of health care policies</li>
                    <li>Taxes</li>
                  </ul>
                  We aggregate this information for each town and provide you
                  with the tools to search through the forest.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          <Col className="mt-5 mt-lg-0" xs={12} lg={3}>
            <Card className="h-100">
              <Card.Body>
                <Card.Title>
                  Analyse and browse with sophisticated tools
                </Card.Title>
                <Card.Text>
                  We offer you a professional way to search for towns and
                  accomodations. Be done with the endless scrolling through
                  lists of listings while knowing 50% is not suitable. We
                  provide you with a table which allows for sophisticated
                  filters and sorting to be used to narrow down the search. Also
                  we offer some special features such as the maximum internet
                  speed at a given address.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
        </Row>
        <Row className="mt-5">
          <Col xs={12} className="text-center">
            <LinkContainer to="/search">
              <Button variant="primary">Start your search now!</Button>
            </LinkContainer>
          </Col>
        </Row>
      </Container>
    );
  }
}

export default WelcomeContent;
