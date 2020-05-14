import React from "react";
import SearchForm, {State as SearchFormState} from "./SearchForm";

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
        return <SearchForm handleSearchFormSubmission={this.handleSearchFormSubmission}/>
    }
}

export default Search