import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch} from "react-router-dom";
import MainPage from "./components/main_paige/main_page";
import LoginPage from "./components/login_page/login_page";
import RecognizePage from "./components/recognize_page/recognize_page";
import SiteFooter from "./components/common/site_footer/site_footer";
import AccountPage from "./components/account/account";
import NewPhoto from "./components/new_photo/new_photo";
import RegistrationPage from './components/registration/registration_page'
import Toloka from "./components/account/toloka/toloka";

// const notFound = () => {
//     return (
//         <div>404</div>
//     );
// }

class App extends Component {
    render() {
        return <React.Fragment>
            <Router>
                <Switch>
                    <Route exact path="/" component={MainPage}/>
                    <Route path="/login" component={LoginPage}/>
                    <Route path="/recognize" component={RecognizePage}/>
                    <Route path="/account" component={AccountPage}/>
                    <Route path="/new_photo" component={NewPhoto}/>
                    <Route path="/registr" component={RegistrationPage}/>
                    <Route path='/toloka' component={Toloka}/>
                    {/*<Route component={notFound}/>*/}
                </Switch>
                <SiteFooter/>
            </Router>
        </React.Fragment>
    }
}

export default App;
