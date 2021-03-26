import React from 'react';
import { Link } from "react-router-dom";

class SiteHeader extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: this.props.value
        }
    }

    render() {
        return (
            <header className="header" >
                <div className="header-container">
                    <Link to="/" className="header-logo" >
                        TextRec
                    </Link>
                    <nav className="header-menu">
                        <div className="header-navigation-container">
                            <ul className="header-navigation">
                                <li className="header-login-list">
                                    <Link to="/login" className="login-button" style={{padding: "10px 20px   "}}>
                                        {this.props.value}
                                    </Link>
                                </li>
                            </ul>
                        </div>
                    </nav>
                </div>
            </header>
        );
    }
}

export default SiteHeader;
