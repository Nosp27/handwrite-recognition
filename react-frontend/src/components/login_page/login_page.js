import React from 'react';
import SiteHeader from "../common/site_header/site_header";
import SiteFooter from "../common/site_footer/site_footer";
import '../common/site_header/site_header.css';
import '../common/site_footer/site_footer.css';
import './login_page.css'

class LoginPage extends React.Component {
    render() {
        return (
            <React.StrictMode>
                <SiteHeader />
                <div>HELLO THERE!</div>
                <SiteFooter />
            </React.StrictMode>
        );
    }
}

export default LoginPage;
