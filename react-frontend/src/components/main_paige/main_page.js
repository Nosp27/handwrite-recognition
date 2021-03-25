import React from 'react';
import SiteHeader from "../common/site_header/site_header";
import FirstBody from "./first_body/first_body";
import SecondBody from "./second_body/second_body";
import ThirdBody from "./third_body/third_body";
import SiteFooter from "../common/site_footer/site_footer";
import './first_body/insert_form.css';
import '../common/site_header/site_header.css';
import './first_body/first_body.css';
import '../common/site_footer/site_footer.css';
import './second_body/second_body.css';
import './third_body/third_body.css';
import './main_page.css'

class MainPage extends React.Component {
    render() {
        return (
            <React.StrictMode>
                <SiteHeader />
                <FirstBody />
                <SecondBody />
                <section className="splitter">
                </section>
                <ThirdBody />
                <SiteFooter />
            </React.StrictMode>
        );
    }
}

export default MainPage;
