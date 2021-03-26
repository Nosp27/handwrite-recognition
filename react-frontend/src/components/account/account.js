import React from 'react';
import './account.css';
import SiteHeader from "../common/site_header/site_header";
import ManualForm from "./manual/manual";

class AccountPage extends React.Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleFileButtonClick = this.handleFileButtonClick.bind(this);
        this.handleFileChange = this.handleFileChange.bind(this);
        this.handleLanguageButtonClick = this.handleLanguageButtonClick.bind(this);
        this.fileInput = React.createRef();
        this.buttonFileInput = React.createRef();
        this.langInput = React.createRef();

        this.state = {
            file: null,
            isLangsHidden: true,
            lang: null,
            allDataInserted: true
        }
    }

    handleFileButtonClick() {
        if (this.fileInput.current) {
            this.fileInput.current.click();
        }
    }

    handleLanguageButtonClick() {
        this.setState({isLangsHidden: false})
    }

    handleFileChange(event) {
        const file = this.fileInput.current.files[0];
        this.setState({file});
    }

    handleSubmit(event) {
        event.preventDefault();

        console.log('vze');
        if (!this.state.file || !this.state.lang) {
            this.setState({allDataInserted: false});
            return;
            // Красим
        }
        window.location.href = "/recognize";
    }

    render() {
        return (
            <React.StrictMode>
                <SiteHeader value={this.props.location.state}/>
                <div className="acc-fb-red-rect">
                </div>
                <div className="forms-cont">
                    <div className="acc-fb-white-rect">
                        <div className="acc-fb-wr-insert-form-container">
                            <div className="acc-insert-form-header">
                                <h2 className="acc-fb-wr-insert-form-label">распознать текст автоматически</h2>
                            </div>
                            <div className="acc-fb-wr-insert-form">
                                <form className="acc-insert-form" onSubmit={this.handleSubmit}>
                                    <div className={`insert-form-button ${
                                        !this.state.allDataInserted && !this.state.file ? 'red-boarder' : ''
                                    }`} ref={this.buttonFileInput} onClick={this.handleFileButtonClick}>
                                        {this.state.file ? this.state.file.name : '► Загрузить фотографию рукописного текста'}
                                    </div>
                                    {/*<div id="file-name"></div>*/}
                                    <input type="file" id="image" accept="image/*" onChange={this.handleFileChange} ref={this.fileInput} />
                                    <label></label>
                                    {/*<div className="acc-insert-form-button" onClick={this.handleLanguageButtonClick} id="file">*/}
                                    {/*    {this.state.lang ? this.state.lang.name : '► Выбрать язык рукописного текста'}*/}
                                    {/*</div>*/}
                                    <div className="acc-insert-form-langs-container" >
                                        <div className={`insert-form-button ${
                                            !this.state.allDataInserted && !this.state.lang ? 'red-boarder' : ''
                                        }`} onClick={this.handleLanguageButtonClick} id="file">
                                            {this.state.lang ? this.state.lang.name : '► Выбрать язык рукописного текста'}
                                        </div>
                                        <div className="acc-insert-form-langs" hidden={this.state.isLangsHidden}>
                                            {
                                                [
                                                    {name: 'Английский', code: 'eng'},
                                                    {name: 'Русский', code: 'russian'}
                                                ].map(({name, code}) => <div
                                                    className={'insert-form-lang'}
                                                    key={code}
                                                    onClick={() => {this.setState({lang: {code, name}, isLangsHidden: true});}}
                                                >{name}</div>)
                                            }
                                        </div>
                                    </div>
                                    <br/>
                                    <div className="acc-insert-form-button submit-button-label" onClick={this.handleSubmit}>
                                        Распознать
                                    </div>
                                    <input type="submit" value="Распознать" id="submit"/>
                                </form>
                            </div>
                        </div>
                        <div className="mf-container">
                            <ManualForm />
                        </div>
                    </div>
                </div>
            </React.StrictMode>
        );
    }
}

export default AccountPage;
