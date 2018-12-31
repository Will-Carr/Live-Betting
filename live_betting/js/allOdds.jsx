import React from 'react';

class AllOdds extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      odds: {}
    };
    this.refreshGame = this.refreshGame.bind(this);
  }

  componentDidMount() {
    // Get game's odds
    this.refreshGame();

    setInterval(() => this.refreshGame(), 5000);
  }

  refreshGame() {
    // Get game's odds
    fetch(this.props.url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          odds: data.odds,
        });
      });
  }

  render() {
    let mainOdds = {
      "team1": {
        "name": "",
        "spread": "",
        "moneyline": "",
        "total": ""
      },
      "team2": {
        "name": "",
        "spread": "",
        "moneyline": "",
        "total": ""
      }
    }

    for(let i = 0; i < this.state.odds.length; i++){
      let odd = this.state.odds[i];
      if(odd["type"] == "spread" && (odd["period"] == "Match" || odd["period"] == "Live Match")){

        if(mainOdds["team1"]["name"] == "" || mainOdds["team1"]["name"] == odd["teams"][0]["team"]){
          mainOdds["team1"]["name"] = odd["teams"][0]["team"]
          mainOdds["team1"]["spread"] = odd["teams"][0]["val"]
        } else if(mainOdds["team1"]["name"] == odd["teams"][1]["team"]){
          mainOdds["team1"]["name"] = odd["teams"][1]["team"]
          mainOdds["team1"]["spread"] = odd["teams"][1]["val"]
        }

        if(mainOdds["team2"]["name"] == "" || mainOdds["team2"]["name"] == odd["teams"][1]["team"]){
          mainOdds["team2"]["name"] = odd["teams"][1]["team"]
          mainOdds["team2"]["spread"] = odd["teams"][1]["val"]
        } else if(mainOdds["team2"]["name"] == "" || mainOdds["team2"]["name"] == odd["teams"][0]["team"]){
          mainOdds["team2"]["name"] = odd["teams"][0]["team"]
          mainOdds["team2"]["spread"] = odd["teams"][0]["val"]
        }

      } else if(odd["type"] == "moneyline" && (odd["period"] == "Match" || odd["period"] == "Live Match")){

        if(mainOdds["team1"]["name"] == "" || mainOdds["team1"]["name"] == odd["teams"][0]["team"]){
          mainOdds["team1"]["name"] = odd["teams"][0]["team"]
          mainOdds["team1"]["moneyline"] = odd["teams"][0]["val"]
        } else if(mainOdds["team1"]["name"] == odd["teams"][1]["team"]){
          mainOdds["team1"]["name"] = odd["teams"][1]["team"]
          mainOdds["team1"]["moneyline"] = odd["teams"][1]["val"]
        }

        if(mainOdds["team2"]["name"] == "" || mainOdds["team2"]["name"] == odd["teams"][1]["team"]){
          mainOdds["team2"]["name"] = odd["teams"][1]["team"]
          mainOdds["team2"]["moneyline"] = odd["teams"][1]["val"]
        } else if(mainOdds["team2"]["name"] == "" || mainOdds["team2"]["name"] == odd["teams"][0]["team"]){
          mainOdds["team2"]["name"] = odd["teams"][0]["team"]
          mainOdds["team2"]["moneyline"] = odd["teams"][0]["val"]
        }

      } else if(odd["type"] == "total" && (odd["period"] == "Match" || odd["period"] == "Live Match")){

        if(mainOdds["team1"]["name"] == "" || mainOdds["team1"]["name"] == odd["teams"][0]["team"]){
          mainOdds["team1"]["name"] = odd["teams"][0]["team"]
          mainOdds["team1"]["total"] = odd["teams"][0]["val"]
        } else if(mainOdds["team1"]["name"] == odd["teams"][1]["team"]){
          mainOdds["team1"]["name"] = odd["teams"][1]["team"]
          mainOdds["team1"]["total"] = odd["teams"][1]["val"]
        }

        if(mainOdds["team2"]["name"] == "" || mainOdds["team2"]["name"] == odd["teams"][1]["team"]){
          mainOdds["team2"]["name"] = odd["teams"][1]["team"]
          mainOdds["team2"]["total"] = odd["teams"][1]["val"]
        } else if(mainOdds["team2"]["name"] == "" || mainOdds["team2"]["name"] == odd["teams"][0]["team"]){
          mainOdds["team2"]["name"] = odd["teams"][0]["team"]
          mainOdds["team2"]["total"] = odd["teams"][0]["val"]
        }

      }
    }


    return (

      <div>
        <table>
          <thead>
            <tr>
              <th></th>
              <th>Spread</th>
              <th>Moneyline</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{mainOdds.team1.name}</td>
              <td>{mainOdds.team1.spread}</td>
              <td>{mainOdds.team1.moneyline}</td>
              <td>{mainOdds.team1.total}</td>
            </tr>
            <tr>
              <td>{mainOdds.team2.name}</td>
              <td>{mainOdds.team2.spread}</td>
              <td>{mainOdds.team2.moneyline}</td>
              <td>{mainOdds.team2.total}</td>
            </tr>
          </tbody>
        </table>
      </div>
    );
  }
}

export default AllOdds;
