import React from "react";
import SearchForm, {State as SearchFormState} from "./SearchForm/SearchForm";
import Container from "react-bootstrap/Container";
import Banner from "../Utilities/Banner";

interface Props {}

interface State {}

class Search extends React.Component<Props, State> {
    constructor(props: Props){
        super(props);
        this.state = {}
        this.handleSearchFormSubmission = this.handleSearchFormSubmission.bind(this);
    }
    handleSearchFormSubmission(
        searchFormState: SearchFormState
    ){
        
    }

    render(){
        return (
            <Container fluid>
                <Banner />
                <SearchForm handleSearchFormSubmission={this.handleSearchFormSubmission}/>
            </Container>
        );
    }
}

export default Search