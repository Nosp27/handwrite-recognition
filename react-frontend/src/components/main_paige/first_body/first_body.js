import React from 'react';
import {Paragraph} from "./paragraph/paragraph";

class FirstBody extends React.Component {
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

        if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
            alert('The File APIs are not fully supported in this browser.');
            return;
        }

        console.log('vze');
<<<<<<< HEAD
        console.log(!this.state.file);
        console.log(this.state.file);
        if (!this.state.file || !this.state.lang) {
=======
        if (!this.state.file || !this.state.lang || !this.state.file[0]) {
>>>>>>> 9ba4a4f1c8375a192d829b25e7911d7accac1947
            this.setState({allDataInserted: false});
            return;
            // Красим
        }
        // window.location.href = "/recognize";
        //
        // const file = this.fileInput.current.files[0];
        // const lang = this.langInput.current.value;
        //
        // const reader = new FileReader();
        // reader.readAsDataURL(file);
        //
        // reader.onload = () => {
        //     const data = reader.result;
        //

<<<<<<< HEAD
        uploadFile(this.state.file, this.state.lang).then(result => {
=======
        uploadFile(file, lang).then(result => {
>>>>>>> 9ba4a4f1c8375a192d829b25e7911d7accac1947
            if (!result) {
                throw new Error("Request id cannot be resolved from response");
            }
            this.setState({"request_id": result["request_id"]});
        });

        console.log(this.state.file);
        console.log(this.state.lang);

        // window.location.href = "/recognize";
        // };
    }

    componentDidMount() {
<<<<<<< HEAD
        this.interval = setInterval(
            () => {
                if (!this.state.request_id) {
                    return;
                }
                fetch(`api/status/?request_id=${this.state.request_id}`)
                    .then(x => {
                        if (x.status === 404)
                            this.setState({"status": "Not Found"});
                        const json_data = x.json();
                        if (json_data["status"] === "done" && json_data["result"])
                            this.setState({"result": json_data["result"]});
                        this.setState({"status": json_data["status"]});
                    });
            }, 3000);
=======
      this.interval = setInterval(
          () => {
              if (!this.state.request_id) {
                  return;
              }
              fetch(`api/status/?request_id=${this.state.request_id}`)
                  .then(x => {
                      if (x.status === 404)
                          this.setState({"status": "Not Found"});
                      const json_data = x.json();
                      if (json_data["status"] === "done" && json_data["result"])
                          this.setState({"result": json_data["result"]});
                      this.setState({"status": json_data["status"]});
                  });
          }, 3000);
>>>>>>> 9ba4a4f1c8375a192d829b25e7911d7accac1947
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    render() {
        return (
            <section className="first-body-container">
                <div className="fb-red-rect">
                </div>
                <div className="fb-white-rect">
                    <div className="fb-wr-insert-form-container">
                        <div className="insert-form-header">
                            <h2 className="fb-wr-insert-form-label">распознать текст</h2>
                        </div>
                        <div className="fb-wr-insert-form">
                            <form className="insert-form" onSubmit={this.handleSubmit}>
                                <div className={`insert-form-button ${
                                    !this.state.allDataInserted && !this.state.file ? 'red-boarder' : ''
                                }`} ref={this.buttonFileInput} onClick={this.handleFileButtonClick}>
                                    {this.state.file ? this.state.file.name : '► Загрузить фотографию рукописного текста'}
                                </div>
                                {/*<div id="file-name"></div>*/}
                                <input type="file" id="image" accept="image/*" onChange={this.handleFileChange} ref={this.fileInput} />
                                <label></label>
                                {/*<div className="insert-form-button" onClick={this.handleLanguageButtonClick} id="file">*/}
                                {/*    {this.state.lang ? this.state.lang.name : '► Выбрать язык рукописного текста'}*/}
                                {/*</div>*/}
                                <div className="insert-form-langs-container" >
                                    <div className={`insert-form-button ${
                                        !this.state.allDataInserted && !this.state.lang ? 'red-boarder' : ''
                                    }`} onClick={this.handleLanguageButtonClick} id="file">
                                        {this.state.lang ? this.state.lang.name : '► Выбрать язык рукописного текста'}
                                    </div>
                                    <div className="insert-form-langs" hidden={this.state.isLangsHidden}>
                                        {
                                            [
                                                {name: 'Английский', code: 'eng'},
                                                {name: 'Итальянский', code: 'italian'}
                                            ].map(({name, code}) => <div
                                                className={'insert-form-lang'}
                                                key={code}
                                                onClick={() => {this.setState({lang: {code, name}, isLangsHidden: true});}}
                                            >{name}</div>)
                                        }
                                    </div>
                                </div>
                                <br/>
                                <div className="insert-form-button submit-button-label" onClick={this.handleSubmit}>
                                    Распознать
                                </div>
                                <input type="submit" value="Распознать" id="submit"/>
                            </form>
                        </div>
                    </div>
                </div>
                <div className="fb-repeated-notes">
                    {
                        [
                            {title: 'Любой текст?', text: 'Правда любой? Круто!'},
                            {title: 'БЫСТРО, ЭЛЕМЕНТАРНО!', text: 'Вау!'},
                            {
                                title: 'ПРИКРЕПИ ФОТОГРАФИЮ КОНСПЕКТА И ПОЛУЧИ РАСПОЗНАННЫЙ ТЕКСТ!',
                                text: 'Не удовлетворен качеством распознавания? Подпишись! Всего за 499р в месяц распознавай любое количество рукописного текста со 100% качеством*!'
                            }
                        ].map(({title, text}, index) => <Paragraph key={index} title={title} text={text}/>)
                    }
                </div>
            </section>
        );
    }
}


async function uploadFile(file, lang) {
    return new Promise(
        (resolve, reject) => {
            const timeout = setTimeout(function () {
                document.getElementById("message-place").innerText = "Timeout Error.";
<<<<<<< HEAD
                reject(new Error("Request timeout"  ));
=======
                reject(new Error("Request timeout"));
>>>>>>> 9ba4a4f1c8375a192d829b25e7911d7accac1947
            }, 60000);

            const reader = new FileReader();
            reader.readAsDataURL(file);

            reader.onload = () => {
                const data = reader.result;

                fetch("api/image_submit/", {
                        method: "POST",
<<<<<<< HEAD
                        mode: 'no-cors',
=======
>>>>>>> 9ba4a4f1c8375a192d829b25e7911d7accac1947
                        body: JSON.stringify({"image": data, "lang": lang})
                    }
                )
                    .then(resp => {
                        clearTimeout(timeout);
                        try {
<<<<<<< HEAD
                            console.log(resp);
=======
>>>>>>> 9ba4a4f1c8375a192d829b25e7911d7accac1947
                            const resp_json = resp.json();
                            resolve(resp_json);
                        } catch (e) {
                        }
                    })
                    .catch(x => {
<<<<<<< HEAD
                        console.error(x);
                        // console.exception(e);
                        // console.error("Server returned: " + resp.status + "; " + resp.text());
=======
                        console.exception(e);
                        console.error("Server returned: " + resp.status + "; " + resp.text());
>>>>>>> 9ba4a4f1c8375a192d829b25e7911d7accac1947
                        reject(x);
                    });
            };
        }
    )
}

export default FirstBody;
