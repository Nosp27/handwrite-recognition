import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch} from "react-router-dom";
import MainPage from "./components/main_paige/main_page";
import LoginPage from "./components/login_page/login_page";
import RecognizePage from "./components/recognize_page/recognize_page";
import SiteHeader from "./components/common/site_header/site_header";
import SiteFooter from "./components/common/site_footer/site_footer";

const notFound = () => {
    return (
        <div>404</div>
    );
}

class App extends Component {
    render() {
        return <React.Fragment>
            <Router>
                <SiteHeader />
                <Switch>
                    <Route exact path="/" component={MainPage}/>
                    <Route path="/login" component={LoginPage}/>
                    <Route path ="/recognize" component={RecognizePage}/>
                    <Route component={notFound}/>
                </Switch>
                <SiteFooter/>
            </Router>
        </React.Fragment>
    }
}

export default App;
