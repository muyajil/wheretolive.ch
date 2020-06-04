import React from "react";
import SearchForm, { State as SearchFormState } from "./SearchForm/SearchForm";
import Container from "react-bootstrap/Container";
import Banner from "../Utilities/Banner";
import publicIp from "public-ip";
import {Redirect} from "react-router-dom";
import Spinner from "react-bootstrap/Spinner";

interface Props {}

interface State {
  showSearchForm: boolean;
  showBanner: boolean;
  searchExecuted: boolean;
  loading: boolean;
}

class Search extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      showSearchForm: true,
      showBanner: true,
      searchExecuted: false,
      loading: false,
    };
    this.handleSearchFormSubmission = this.handleSearchFormSubmission.bind(
      this
    );
  }
  handleSearchFormSubmission(searchFormState: SearchFormState) {
    if (searchFormState.selectedTown.length >= 1) {
      const ipAddress = publicIp.v4();
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          selectedTown: searchFormState.selectedTown[0],
          commuteTime: searchFormState.commuteTime,
          onlyTrainCommute: searchFormState.onlyTrainCommute,
          income: searchFormState.income,
          numChildren: searchFormState.numChildren,
          married: searchFormState.married,
          doubleSalary: searchFormState.doubleSalary,
          birthYears: searchFormState.birthYears,
          franchises: searchFormState.franchises,
          minRooms: searchFormState.minRooms,
          maxRooms: searchFormState.maxRooms,
          minArea: searchFormState.minArea,
          maxArea: searchFormState.maxArea,
          offerType: searchFormState.offerType,
          public_ip: ipAddress,
        }),
      };
      this.setState({ loading: true, showSearchForm: false, showBanner: false }, () =>
        fetch(process.env.REACT_APP_BACKEND_URL + "/search/", requestOptions)
          .then((response) => response.json())
          .then((data) => {
            localStorage.setItem("searchResults", JSON.stringify(data));
            this.setState({
              searchExecuted: true,
              loading: false,
            });
          })
      );
    }
  }

  renderSearchForm() {
    if (this.state.showSearchForm) {
      return (
        <SearchForm
          handleSearchFormSubmission={this.handleSearchFormSubmission}
        />
      );
    }
  }

  renderBanner() {
    if (this.state.showBanner) {
      return <Banner />;
    }
  }

  render() {
    if (this.state.searchExecuted){
      return (
        <Redirect to="/search/towns" />
      );
    } else {
      return (
        <Container fluid>
        {this.renderBanner()}
        {this.renderSearchForm()}
        {this.state.loading ? (
          <Spinner className="mx-auto" animation="border" variant="light"/>
        ) : null}
        </Container>
    );
    }
  }
}

export default Search;
