import React from 'react';

class AllOdds extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      sport: "",
      odds: {},
      prevOdds: {
        "team1": {
          "name": "",
          "spread": {
            "spread": "",
            "change": "none"
          },
          "moneyline": {
            "moneyline": "",
            "change": "none"
          },
          "total": {
            "total": "",
            "change": "none"
          }
        },
        "team2": {
          "name": "",
          "spread": {
            "spread": "",
            "change": "none"
          },
          "moneyline": {
            "moneyline": "",
            "change": "none"
          },
          "total": {
            "total": "",
            "change": "none"
          }
        }
      },
      live_stats: "<div></div>"
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
          sport: data.sport,
          odds: data.odds,
          live_stats: data.live_stats,
        });
      });
  }

  render() {
    let mainOdds = {
      "team1": {
        "name": "",
        "spread": {
          "spread": "",
          "change": "none"
        },
        "moneyline": {
          "moneyline": "",
          "change": "none"
        },
        "total": {
          "total": "",
          "change": "none"
        }
      },
      "team2": {
        "name": "",
        "spread": {
          "spread": "",
          "change": "none"
        },
        "moneyline": {
          "moneyline": "",
          "change": "none"
        },
        "total": {
          "total": "",
          "change": "none"
        }
      },
      "team3": {
        "name": "",
        "spread": {
          "spread": "",
          "change": "none"
        },
        "moneyline": {
          "moneyline": "",
          "change": "none"
        },
        "total": {
          "total": "",
          "change": "none"
        }
      }
    }

    let prevOdds = this.state.prevOdds;
    let sport = this.state.sport;

    for(let i = 0; i < this.state.odds.length; i++){
      try {
        let odd = this.state.odds[i];
        if(odd["type"] == "spread" && (odd["period"] == "Match" || odd["period"] == "Live Match" || odd["period"] == "Regulation Time" || odd["period"] == "Live Regulation Time")){

          if(mainOdds["team1"]["name"] == "" || mainOdds["team1"]["name"] == odd["teams"][0]["team"]){
            mainOdds["team1"]["name"] = odd["teams"][0]["team"]

            if(parseFloat(odd["teams"][0]["val"]) > parseFloat(prevOdds["team1"]["spread"]["spread"])){
              mainOdds["team1"]["spread"]["change"] = "inc";
            } else if(parseFloat(odd["teams"][0]["val"]) < parseFloat(prevOdds["team1"]["spread"]["spread"])){
              mainOdds["team1"]["spread"]["change"] = "dec";
            } else {
              mainOdds["team1"]["spread"]["change"] = "none";
            }

            mainOdds["team1"]["spread"]["spread"] = odd["teams"][0]["val"]
          } else if(mainOdds["team1"]["name"] == odd["teams"][1]["team"]){
            mainOdds["team1"]["name"] = odd["teams"][1]["team"]

            if(parseFloat(odd["teams"][1]["val"]) > parseFloat(prevOdds["team1"]["spread"]["spread"])){
              mainOdds["team1"]["spread"]["change"] = "inc";
            } else if(parseFloat(odd["teams"][1]["val"]) < parseFloat(prevOdds["team1"]["spread"]["spread"])){
              mainOdds["team1"]["spread"]["change"] = "dec";
            } else {
              mainOdds["team1"]["spread"]["change"] = "none";
            }

            mainOdds["team1"]["spread"]["spread"] = odd["teams"][1]["val"]
          }

          if(mainOdds["team2"]["name"] == "" || mainOdds["team2"]["name"] == odd["teams"][1]["team"]){
            mainOdds["team2"]["name"] = odd["teams"][1]["team"]

            if(parseFloat(odd["teams"][1]["val"]) > parseFloat(prevOdds["team2"]["spread"]["spread"])){
              mainOdds["team2"]["spread"]["change"] = "inc";
            } else if(parseFloat(odd["teams"][1]["val"]) < parseFloat(prevOdds["team2"]["spread"]["spread"])){
              mainOdds["team2"]["spread"]["change"] = "dec";
            } else {
              mainOdds["team2"]["spread"]["change"] = "none";
            }

            mainOdds["team2"]["spread"]["spread"] = odd["teams"][1]["val"]
          } else if(mainOdds["team2"]["name"] == "" || mainOdds["team2"]["name"] == odd["teams"][0]["team"]){
            mainOdds["team2"]["name"] = odd["teams"][0]["team"]

            if(parseFloat(odd["teams"][0]["val"]) > parseFloat(prevOdds["team2"]["spread"]["spread"])){
              mainOdds["team2"]["spread"]["change"] = "inc";
            } else if(parseFloat(odd["teams"][0]["val"]) < parseFloat(prevOdds["team2"]["spread"]["spread"])){
              mainOdds["team2"]["spread"]["change"] = "dec";
            } else {
              mainOdds["team2"]["spread"]["change"] = "none";
            }

            mainOdds["team2"]["spread"]["spread"] = odd["teams"][0]["val"]
          }

        } else if(odd["type"] == "moneyline" && (odd["period"] == "Match" || odd["period"] == "Live Match" || odd["period"] == "Regulation Time" || odd["period"] == "Live Regulation Time")){

          if(mainOdds["team1"]["name"] == "" || mainOdds["team1"]["name"] == odd["teams"][0]["team"]){
            mainOdds["team1"]["name"] = odd["teams"][0]["team"]

            if(parseFloat(odd["teams"][0]["val"]) > parseFloat(prevOdds["team1"]["moneyline"]["moneyline"])){
              mainOdds["team1"]["moneyline"]["change"] = "inc";
            } else if(parseFloat(odd["teams"][0]["val"]) < parseFloat(prevOdds["team1"]["moneyline"]["moneyline"])){
              mainOdds["team1"]["moneyline"]["change"] = "dec";
            } else {
              mainOdds["team1"]["moneyline"]["change"] = "none";
            }

            mainOdds["team1"]["moneyline"]["moneyline"] = odd["teams"][0]["val"]
          } else if(mainOdds["team1"]["name"] == odd["teams"][1]["team"]){
            mainOdds["team1"]["name"] = odd["teams"][1]["team"]

            if(parseFloat(odd["teams"][1]["val"]) > parseFloat(prevOdds["team1"]["moneyline"]["moneyline"])){
              mainOdds["team1"]["moneyline"]["change"] = "inc";
            } else if(parseFloat(odd["teams"][1]["val"]) < parseFloat(prevOdds["team1"]["moneyline"]["moneyline"])){
              mainOdds["team1"]["moneyline"]["change"] = "dec";
            } else {
              mainOdds["team1"]["moneyline"]["change"] = "none";
            }

            mainOdds["team1"]["moneyline"]["moneyline"] = odd["teams"][1]["val"]
          } else if(sport == "soccer" && mainOdds["team1"]["name"] == odd["teams"][2]["team"]){
            mainOdds["team1"]["name"] = odd["teams"][2]["team"]

            if(parseFloat(odd["teams"][2]["val"]) > parseFloat(prevOdds["team1"]["moneyline"]["moneyline"])){
              mainOdds["team1"]["moneyline"]["change"] = "inc";
            } else if(parseFloat(odd["teams"][2]["val"]) < parseFloat(prevOdds["team1"]["moneyline"]["moneyline"])){
              mainOdds["team1"]["moneyline"]["change"] = "dec";
            } else {
              mainOdds["team1"]["moneyline"]["change"] = "none";
            }

            mainOdds["team1"]["moneyline"]["moneyline"] = odd["teams"][2]["val"]
          }

          // HERE
          if(mainOdds["team2"]["name"] == "" || mainOdds["team2"]["name"] == odd["teams"][1]["team"]){
            mainOdds["team2"]["name"] = odd["teams"][1]["team"]

            if(parseFloat(odd["teams"][1]["val"]) > parseFloat(prevOdds["team2"]["moneyline"]["moneyline"])){
              mainOdds["team2"]["moneyline"]["change"] = "inc";
            } else if(parseFloat(odd["teams"][1]["val"]) < parseFloat(prevOdds["team2"]["moneyline"]["moneyline"])){
              mainOdds["team2"]["moneyline"]["change"] = "dec";
            } else {
              mainOdds["team2"]["moneyline"]["change"] = "none";
            }

            mainOdds["team2"]["moneyline"]["moneyline"] = odd["teams"][1]["val"]
          } else if(mainOdds["team2"]["name"] == odd["teams"][0]["team"]){
            mainOdds["team2"]["name"] = odd["teams"][0]["team"]

            if(parseFloat(odd["teams"][0]["val"]) > parseFloat(prevOdds["team2"]["moneyline"]["moneyline"])){
              mainOdds["team2"]["moneyline"]["change"] = "inc";
            } else if(parseFloat(odd["teams"][0]["val"]) < parseFloat(prevOdds["team2"]["moneyline"]["moneyline"])){
              mainOdds["team2"]["moneyline"]["change"] = "dec";
            } else {
              mainOdds["team2"]["moneyline"]["change"] = "none";
            }

            mainOdds["team2"]["moneyline"]["moneyline"] = odd["teams"][0]["val"]
          } else if(sport == "soccer" && mainOdds["team2"]["name"] == odd["teams"][2]["team"]){
            mainOdds["team2"]["name"] = odd["teams"][2]["team"]

            if(parseFloat(odd["teams"][2]["val"]) > parseFloat(prevOdds["team2"]["moneyline"]["moneyline"])){
              mainOdds["team2"]["moneyline"]["change"] = "inc";
            } else if(parseFloat(odd["teams"][2]["val"]) < parseFloat(prevOdds["team2"]["moneyline"]["moneyline"])){
              mainOdds["team2"]["moneyline"]["change"] = "dec";
            } else {
              mainOdds["team2"]["moneyline"]["change"] = "none";
            }

            mainOdds["team2"]["moneyline"]["moneyline"] = odd["teams"][2]["val"]
          }

          if(sport == "soccer" && (mainOdds["team3"]["name"] == "" || mainOdds["team3"]["name"] == odd["teams"][2]["team"])){
            mainOdds["team3"]["name"] = odd["teams"][2]["team"]

            if(parseFloat(odd["teams"][2]["val"]) > parseFloat(prevOdds["team3"]["moneyline"]["moneyline"])){
              mainOdds["team3"]["moneyline"]["change"] = "inc";
            } else if(parseFloat(odd["teams"][2]["val"]) < parseFloat(prevOdds["team3"]["moneyline"]["moneyline"])){
              mainOdds["team3"]["moneyline"]["change"] = "dec";
            } else {
              mainOdds["team3"]["moneyline"]["change"] = "none";
            }

            mainOdds["team3"]["moneyline"]["moneyline"] = odd["teams"][2]["val"]
          } else if(sport == "soccer" && mainOdds["team3"]["name"] == odd["teams"][1]["team"]){
            mainOdds["team3"]["name"] = odd["teams"][1]["team"]

            if(parseFloat(odd["teams"][1]["val"]) > parseFloat(prevOdds["team3"]["moneyline"]["moneyline"])){
              mainOdds["team3"]["moneyline"]["change"] = "inc";
            } else if(parseFloat(odd["teams"][1]["val"]) < parseFloat(prevOdds["team3"]["moneyline"]["moneyline"])){
              mainOdds["team3"]["moneyline"]["change"] = "dec";
            } else {
              mainOdds["team3"]["moneyline"]["change"] = "none";
            }

            mainOdds["team3"]["moneyline"]["moneyline"] = odd["teams"][1]["val"]
          } else if(sport == "soccer" && mainOdds["team3"]["name"] == odd["teams"][0]["team"]){
            mainOdds["team3"]["name"] = odd["teams"][0]["team"]

            if(parseFloat(odd["teams"][0]["val"]) > parseFloat(prevOdds["team3"]["moneyline"]["moneyline"])){
              mainOdds["team3"]["moneyline"]["change"] = "inc";
            } else if(parseFloat(odd["teams"][0]["val"]) < parseFloat(prevOdds["team3"]["moneyline"]["moneyline"])){
              mainOdds["team3"]["moneyline"]["change"] = "dec";
            } else {
              mainOdds["team3"]["moneyline"]["change"] = "none";
            }

            mainOdds["team3"]["moneyline"]["moneyline"] = odd["teams"][0]["val"]
          }

        } else if(odd["type"] == "total" && (odd["period"] == "Match" || odd["period"] == "Live Match" || odd["period"] == "Regulation Time" || odd["period"] == "Live Regulation Time")){

          if(mainOdds["team1"]["name"] == "" || mainOdds["team1"]["name"] == odd["teams"][0]["team"]){
            mainOdds["team1"]["name"] = odd["teams"][0]["team"]

            if(parseFloat(odd["teams"][0]["val"].substring(2)) > parseFloat(prevOdds["team1"]["total"]["total"].substring(2))){
              mainOdds["team1"]["total"]["change"] = "inc";
            } else if(parseFloat(odd["teams"][0]["val"].substring(2)) < parseFloat(prevOdds["team1"]["total"]["total"].substring(2))){
              mainOdds["team1"]["total"]["change"] = "dec";
            } else {
              mainOdds["team1"]["total"]["change"] = "none";
            }

            mainOdds["team1"]["total"]["total"] = odd["teams"][0]["val"]
          } else if(mainOdds["team1"]["name"] == odd["teams"][1]["team"]){
            mainOdds["team1"]["name"] = odd["teams"][1]["team"]

            if(parseFloat(odd["teams"][1]["val"].substring(2)) > parseFloat(prevOdds["team1"]["total"]["total"].substring(2))){
              mainOdds["team1"]["total"]["change"] = "inc";
            } else if(parseFloat(odd["teams"][1]["val"].substring(2)) < parseFloat(prevOdds["team1"]["total"]["total"].substring(2))){
              mainOdds["team1"]["total"]["change"] = "dec";
            } else {
              mainOdds["team1"]["total"]["change"] = "none";
            }

            mainOdds["team1"]["total"]["total"] = odd["teams"][1]["val"]
          }

          if(mainOdds["team2"]["name"] == "" || mainOdds["team2"]["name"] == odd["teams"][1]["team"]){
            mainOdds["team2"]["name"] = odd["teams"][1]["team"]

            if(parseFloat(odd["teams"][1]["val"].substring(2)) > parseFloat(prevOdds["team2"]["total"]["total"].substring(2))){
              mainOdds["team2"]["total"]["change"] = "inc";
            } else if(parseFloat(odd["teams"][1]["val"].substring(2)) < parseFloat(prevOdds["team2"]["total"]["total"].substring(2))){
              mainOdds["team2"]["total"]["change"] = "dec";
            } else {
              mainOdds["team2"]["total"]["change"] = "none";
            }

            mainOdds["team2"]["total"]["total"] = odd["teams"][1]["val"]
          } else if(mainOdds["team2"]["name"] == "" || mainOdds["team2"]["name"] == odd["teams"][0]["team"]){
            mainOdds["team2"]["name"] = odd["teams"][0]["team"]

            if(parseFloat(odd["teams"][0]["val"].substring(2)) > parseFloat(prevOdds["team2"]["total"]["total"].substring(2))){
              mainOdds["team2"]["total"]["change"] = "inc";
            } else if(parseFloat(odd["teams"][0]["val"].substring(2)) < parseFloat(prevOdds["team2"]["total"]["total"].substring(2))){
              mainOdds["team2"]["total"]["change"] = "dec";
            } else {
              mainOdds["team2"]["total"]["change"] = "none";
            }


            mainOdds["team2"]["total"]["total"] = odd["teams"][0]["val"]
          }

        }
      } catch(err) {}
    }


    this.state.prevOdds = mainOdds;


    return (

      <div>
        <h1>
          {mainOdds.team1.name != "" ? mainOdds.team1.name + " vs. " + mainOdds.team2.name : "No Matchup Found"}
        </h1>
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
              <td className={mainOdds.team1.spread.change}>{mainOdds.team1.spread.spread} <i className={mainOdds.team1.spread.change}></i></td>
              <td className={mainOdds.team1.moneyline.change}>{mainOdds.team1.moneyline.moneyline} <i className={mainOdds.team1.moneyline.change}></i></td>
              <td className={mainOdds.team1.total.change}>{mainOdds.team1.total.total} <i className={mainOdds.team1.total.change}></i></td>
            </tr>
            <tr>
              <td>{mainOdds.team2.name}</td>
              <td className={mainOdds.team2.spread.change}>{mainOdds.team2.spread.spread} <i className={mainOdds.team2.spread.change}></i></td>
              <td className={mainOdds.team2.moneyline.change}>{mainOdds.team2.moneyline.moneyline} <i className={mainOdds.team2.moneyline.change}></i></td>
              <td className={mainOdds.team2.total.change}>{mainOdds.team2.total.total} <i className={mainOdds.team2.total.change}></i></td>
            </tr>
            {mainOdds.team3.name != "" ? <tr>
              <td>{mainOdds.team3.name}</td>
              <td className={mainOdds.team3.spread.change}>{mainOdds.team3.spread.spread} <i className={mainOdds.team3.spread.change}></i></td>
              <td className={mainOdds.team3.moneyline.change}>{mainOdds.team3.moneyline.moneyline} <i className={mainOdds.team3.moneyline.change}></i></td>
              <td className={mainOdds.team3.total.change}>{mainOdds.team3.total.total} <i className={mainOdds.team3.total.change}></i></td>
            </tr> : ""}
          </tbody>
        </table>
        <br />
        <div dangerouslySetInnerHTML={{__html: this.state.live_stats}}></div>
      </div>
    );
  }
}

export default AllOdds;
