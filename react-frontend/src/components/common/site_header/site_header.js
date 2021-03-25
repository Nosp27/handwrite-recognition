import React from 'react';
import { Link } from "react-router-dom";

class SiteHeader extends React.Component {
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
                                    {/*TODO проверка на какой я странице, если не на логина, то показывать лк*/}
                                    <Link to="/login" className="login-button" style={{padding: "10px 20px   "}}>
                                        Личный кабинет
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
