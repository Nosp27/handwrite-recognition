import React from 'react';
import './account.css';
import SiteHeader from "../common/site_header/site_header";

class AccountPage extends React.Component {

    render() {
        return (
            <React.StrictMode>
                <SiteHeader value={"Привет, " + this.props.location.state + "!"}/>
                <div className="fb-red-rect">
                </div>
                <div className="fb-white-rect">
                    <div className="fb-wr-insert-form-container">
                        <div className="insert-form-header">
                            <h2 className="fb-wr-insert-form-label">ор</h2>
                        </div>
                    </div>
                </div>
            </React.StrictMode>
        );
    }
}

export default AccountPage;
