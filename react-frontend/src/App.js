import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch, Link, Redirect} from "react-router-dom";
import MainPage from "./components/main_paige/main_page";
import LoginPage from "./components/login_page/login_page";

const notFound = () => {
    return (
        <div>404</div>
    );
}

class App extends Component {
    render() {
        return <Router>
            <Switch>
                <Route exact path="/" component={MainPage}/>
                <Route path="/login" component={LoginPage}/>
                <Route component={notFound}/>
            </Switch>
        </Router>
    }
}

export default App;
