import React from 'react';
import '../common/site_footer/site_footer.css';
import './recognize_page.css'
import SiteHeader from "../common/site_header/site_header";
import {Link} from "react-router-dom";


class RecognizePage extends React.Component {
    render() {
        return (
            <React.StrictMode>
                <SiteHeader value="Личный кабинет"/>
                <div className="rec-page-container">
                    <div className="rp-main-container">
                        <div className="white-rect">
                            <div className="text-title">Распознанный текст</div>
                            <div className="text-body">{"I'm a cat!"}</div>
                        </div>
                        <Link to='/new_photo' className="rp-button wrong" onClick={this.onWrongButtonClick}>
                            ЭТО НЕПРАВИЛЬНО
                        </Link>
                        <Link to='/' className="rp-button other">
                            РАСПОЗНАТЬ ДРУГОЙ ТЕКСТ
                        </Link>
                    </div>

                </div>
            </React.StrictMode>
        );
    }
}

export default RecognizePage;
