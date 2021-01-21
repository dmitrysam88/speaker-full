import './App.css';
import axios from 'axios';
import { useState } from 'react';
import ReactAudioPlayer from 'react-audio-player';

function App() {

  const [mainText, setMainText] = useState('');
  const [audioLink, setAudioLink] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [lang, setLang] = useState('en');

  const onSpeack = () => {
    setIsLoading(true);
    axios.post('/api/speak', { text: mainText, lang: lang }).then((resp) => {
      // console.log(resp.data.fileName);
      setAudioLink(resp.data.fileName);
      setIsLoading(false);
    }).catch((error) => {
      console.log(error);
      setIsLoading(false);
    });
  }

  const onChangeText = (event) => {
    setMainText(event.target.value);
  }

  const onChangeLang = (event) => {
    setLang(event.target.value);
  }

  return (
    <div className="App">
      <div className="form-style-6">
        <textarea className="main-text-area" onChange={onChangeText} rows="10" cols="45" value={mainText}></textarea>
        {/* <div className="controls"> */}
          <input type="button" value="Speack" onClick={onSpeack}/>
          <select className="lang-select" value={lang} onChange={onChangeLang}>
            {['en', 'ru', 'ua'].map((el) => {
              return <option value={el}>{el}</option>
            })}
          </select>
        {/* </div> */}
        {isLoading && <div className="spinner"></div>}
        {audioLink && <ReactAudioPlayer src={audioLink} controls />}
      </div>
    </div>
  );
}

export default App;
