import React from 'react';
import './login_page.css'
import {Link} from "react-router-dom";
import SiteHeader from "../common/site_header/site_header";

class LoginPage extends React.Component {
    constructor(props) {
        super(props);
        this.handleEnterChange = this.handleEnterChange.bind(this);
        this.state = {
            login: null,
            password: null
        };
    }

    handleEnterChange(e) {
        this.setState({login: e.target.value});
    }

    render() {
        const login = this.state.login;
        return (
            <React.StrictMode>
                <SiteHeader value="" />
                <div className="lp-rec-page-container">
                    <div className="lp-white-rect">
                        <div className="lp-text-title">АВТОРИЗАЦИЯ</div>
                        <div className="lp-text-body">
                            <input
                                className={'input'}
                                placeholder={'Введите логин'}
                                value={login}
                                onChange={this.handleEnterChange}
                            />
                            <input type="password"
                                className={'input'}
                                placeholder={'Введите пароль'}
                            />
                            <div
                                className={'button-container'}
                            >
                                <Link to={{pathname: "/account", state: login}} className={'button'} >
                                    войти
                                </Link>
                                <Link to="/account" className={'button register'}>
                                    зарегистрироваться
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
            </React.StrictMode>
        );
    }
}

export default LoginPage;
