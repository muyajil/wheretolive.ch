import React from "react";
import SearchForm, { State as SearchFormState } from "./SearchForm/SearchForm";
import Container from "react-bootstrap/Container";
import Banner from "../Utilities/Banner";
import publicIp from "public-ip";
import TownsOverview from "./TownsOverview";
import Spinner from "react-bootstrap/Spinner";

interface Props {}

interface State {
  showSearchForm: boolean;
  showBanner: boolean;
  searchExecuted: boolean;
  loading: boolean;
  responseData: Map<string, object>;
}

class Search extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      showSearchForm: true,
      showBanner: true,
      searchExecuted: false,
      loading: false,
      responseData: new Map<string, object>(),
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
            this.setState({
              responseData: data,
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

  renderTownsOverview() {
    if (this.state.searchExecuted) {
      return (
        <TownsOverview rowData={Object.values(this.state.responseData)} />
      );
    }
  }

  render() {
    return (
      <Container fluid>
        {this.renderBanner()}
        {this.renderSearchForm()}
        {this.state.loading ? (
          <Spinner animation="border" variant="light"/>
        ) : (
          this.renderTownsOverview()
        )}
      </Container>
    );
  }
}

export default Search;
