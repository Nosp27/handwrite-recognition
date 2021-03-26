import React from 'react';
import '../common/site_footer/site_footer.css';
import './recognize_page.css'
import SiteHeader from "../common/site_header/site_header";
import {Link} from "react-router-dom";


class RecognizePage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    componentDidMount() {
        const request_id = this.props.location.search.split("=")[1];
        console.log(request_id);
        this.interval = setInterval(
            () => {
                if (!request_id || this.state.result !== undefined) {
                    return;
                }
                fetch(`api/status/?request_id=${request_id}`)
                    .then(
                        response => {
                            if (response.status === 404)
                                this.setState({"status": "Not Found"});
                            return response.json();
                        }
                    )
                    .then(json_data => {
                        console.log(json_data);
                        if (json_data["status"] === "done" && json_data["result"]) {
                            this.setState({"result": json_data["result"]});
                        }
                        this.setState({"status": json_data["status"]});
                    });
            }, 3000);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    render() {
        return (
            <React.StrictMode>
                <SiteHeader value="Личный кабинет"/>
                <div className="rec-page-container">
                    <div className="rp-main-container">
                        <div className="white-rect">
                            <div className="text-title">Статус</div>
                            <div className="text-body">{this.state.status ? this.state.status : "Ожидание статуса..."}</div>
                        </div>
                        <div className="white-rect">
                            <div className="text-title">Распознанный текст</div>
                            <div className="text-body">{this.state.result ? this.state.result : "Подождите..."}</div>
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
