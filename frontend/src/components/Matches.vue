<template>
  <div id="app" class="container">
    <div class="container">
      <header class="d-flex justify-content-between py-3 mb-4 border-bottom">
        <h1 class="fs-4 mb-3 mb-md-0 me-md-auto"> {{ title }} </h1>
        <div class="d-flex flex-row align-items-center" >
          <div class="mx-2 d-flex flex-row" v-if="logged">
          <img class="mx-2" height="20" src="@/assets/user.png"/>
          <p class="font-weight-bold">{{username}}</p>
          </div>
          <p v-if="logged" class="mx-2 font-weight-bold" >&#128176; {{money_available}}€</p>
          <button v-if="is_admin === 0" class="btn btn-outline-primary mx-2" :disabled="logged === false"  @click="veureCistella()">{{titleCistella}} <span v-if="logged" class="bg-primary text-white p-1 mb-2">{{matches_added.length}}</span> <span v-if="logged" class="bg-primary text-white p-1 mb-2">{{cistellaTotalMoney}} €</span></button>
          <button class="btn btn-outline-primary mx-2" @click="$router.push('/userlogin')">
            {{titleLogin}}
          </button>
        </div>
      </header>
    </div>
    <div v-if="is_showing_cart" class="container">
      <div class="col-lg-12 grid-margin stretch-card">
      <div style="margin-left:auto;margin-right:auto;" class="card">
        <div class="card-body">
          <h4 class="card-title">Cart</h4>
          <div class="table-responsive">
            <table v-if="matches_added.length > 0" style="margin-left:auto;margin-right:auto;" class="table">
              <thead>
                <tr>
                  <th>Sport</th>
                  <th>Competition</th>
                  <th>Match</th>
                  <th>Quantity</th>
                  <th>Price(€)</th>
                  <th>Total</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(match) in matches_added" :key="match.id">
                  <th scope="row">{{ match.competition.sport  }}</th>
                  <td>{{ match.competition.name}}</td>
                  <td><strong>{{ match.local.name }}</strong> ({{ match.local.country }}) vs <strong>{{ match.visitor.name }}</strong> ({{ match.visitor.country }})</td>
                  <td>
                    {{ match.tickets_bought}}
                    <button class="badge badge-danger" @click="deleteOneTicket(match)">-</button>
                    <button class="badge badge-success" :disabled="dissableAddTicket(match)" @click="addOneTicket(match)">+</button>
                  </td>
                  <td>{{ match.price}} &euro;</td>
                  <th>
                    <button class="badge badge-danger" @click="deleteMatch(match)">Eliminar entrada</button>
                  </th>
                </tr>
              </tbody>
            </table>
            <h6 v-else class="card-title">Your cart is currently empty</h6>
          </div>
          <button class="btn btn-secondary"  @click="veureCistella()">Enrere</button>
          <button @click="finalizePurchase" :disabled="matches_added.length === 0" class="btn btn-success">Finalitzar la compra</button>
        </div>
      </div>
    </div>
    </div>
    <div v-else class="container">
      <div class="card-deck" style="background-color: white">
      <div class="col"  style="margin-top: 10px" v-for="(match) in matches" :key="match.id">
        <div class="card mx-auto" style="width: 20rem;" >
        <img class="card-img-top" height="180" :src="require('@/assets/'+match.competition.sport+'.jpg')" alt="Card image cap">
        <div class="card-body">
          <h5>{{ match.competition.sport }} - {{ match.competition.category }}</h5>
          <h6>{{ match.competition.name }}</h6>
          <h6><strong>{{ match.local.name }}</strong> ({{ match.local.country }}) vs <strong>{{ match.visitor.name }}</strong> ({{ match.visitor.country }})</h6>
          <h6>{{ match.date.substring(0,10) }}</h6>
          <h6>{{ match.price }} &euro;</h6>
          <h6> Entrades disponibles {{ match.total_available_tickets - match.tickets_bought }} </h6>
          <button class="btn btn-success btn-lg position-relative fixed-bottom" :disabled="disableAddMatch(match)" @click="addEventToCart(match)">Afegeix a la cistella</button>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <button v-if="is_admin === 1" class="btn btn-success badge-danger btn-lg position-relative fixed-bottom" @click="deleteMatchFromBD(match)">Suprimeix match</button>
        </div>
        </div>
      </div>
      <div v-if="is_admin === 1" class="col"  style="margin-top: 10px">
        <div class="card mx-auto" style="width: 20rem;" >
        <img class="card-img-top" height="180" :src="require('@/assets/question_mark.jpg')" alt="Card image cap">
        <div class="card-body">
          <template>
            <div>
              <button v-b-modal.modal-prevent-closing class="btn btn-success btn-lg position-relative fixed-bottom">Create match</button>

              <b-modal
                id="modal-prevent-closing"
                ref="modal"
                title="Submit Your Match"
                @show="resetModal"
                @hidden="resetModal"
                @ok="handleOk"
              >
                <form ref="form" @submit.stop.prevent="handleSubmit">
                  <b-form-group
                    label="Local id"
                    label-for="name-input"
                    invalid-feedback="Local is required"
                    :state="nameState"
                  >
                    <b-form-input
                      id="name-input"
                      v-model="addNewMatch.local"
                      :state="nameState"
                      required
                    ></b-form-input>
                  </b-form-group>

                  <b-form-group
                    label="Visitor id"
                    label-for="name-input"
                    invalid-feedback="Visitor is required"
                    :state="nameState"
                  >
                    <b-form-input
                      id="name-input"
                      v-model="addNewMatch.visitor"
                      :state="nameState"
                      required
                    ></b-form-input>
                  </b-form-group>

                  <b-form-group
                    label="Date match (format: YYYY-MM-DD)"
                    label-for="name-input"
                    invalid-feedback="Date is required"
                    :state="nameState"
                  >
                    <b-form-input
                      id="name-input"
                      v-model="addNewMatch.date"
                      :state="nameState"
                      required
                    ></b-form-input>
                  </b-form-group>

                  <b-form-group
                    label="Price match"
                    label-for="name-input"
                    invalid-feedback="Price is required"
                    :state="nameState"
                  >
                    <b-form-input
                      id="name-input"
                      v-model="addNewMatch.price"
                      :state="nameState"
                      required
                    ></b-form-input>
                  </b-form-group>

                  <b-form-group
                    label="Competition id"
                    label-for="name-input"
                    invalid-feedback="Competition is required"
                    :state="nameState"
                  >
                    <b-form-input
                      id="name-input"
                      v-model="addNewMatch.competition"
                      :state="nameState"
                      required
                    ></b-form-input>
                  </b-form-group>

                  <b-form-group
                    label="Total available tickets"
                    label-for="name-input"
                    invalid-feedback="Available tickets is required"
                    :state="nameState"
                  >
                    <b-form-input
                      id="name-input"
                      v-model="addNewMatch.total_available_tickets"
                      :state="nameState"
                      required
                    ></b-form-input>
                  </b-form-group>
                </form>
              </b-modal>
            </div>
          </template>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        </div>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios'
import { Alert } from '../../bootstrap/js/bootstrap.bundle'

export default {
    data() {
        return {
            is_showing_cart: false,
            title: "Sport Matches",
            titleCistella: "Veure Cistella",
            titleLogin: "Log in",
            money_available: 0,
            cistellaTotalMoney: 0,
            matches: [],
            matches_added: [],
            logged: false,
            username: "not logged",
            token: "",
            is_admin: false,

            name: '',
            nameState: null,
            addNewMatch: {
              local: '',
              visitor:  '',
              competition: '',
              date: '',
              price: '',
              total_available_tickets: ''
            }
        };
    },
    methods: {
        addEventToCart(match) {
            this.cistellaTotalMoney = Math.round((this.cistellaTotalMoney + match.price) * 100) / 100;
            match.tickets_bought = 1;
            this.matches_added.push(match);
        },
        veureCistella() {
            if (this.is_showing_cart) {
                this.is_showing_cart = false;
                this.titleCistella = "Veure cistella";
            }
            else {
                this.is_showing_cart = true;
                this.titleCistella = "Tanca cistella";
            }
        },
        getAccount() {
            const pathAccount = "https://a12-sportsmaster1.herokuapp.com/account/" + this.username;
            axios.get(pathAccount)
                .then((res) => {
                this.is_admin = res.data.account.is_admin;
                this.money_available = parseFloat(res.data.account.available_money);
            });
        },
        getMatches() {
            const pathMatches = "https://a12-sportsmaster1.herokuapp.com/matches";
            const pathCompetition = "https://a12-sportsmaster1.herokuapp.com/competition/";
            axios.get(pathMatches)
                .then((res) => {
                var matches = res.data.matches.filter((match) => {
                    return match.competition_id != null;
                });
                var promises = [];
                for (let i = 0; i < matches.length; i++) {
                    matches[i].tickets_bought = 0;
                    const promise = axios.get(pathCompetition + matches[i].competition_id)
                        .then((resCompetition) => {
                        delete matches[i].competition_id;
                        matches[i].competition = {
                            "name": resCompetition.data.competition.name,
                            "category": resCompetition.data.competition.category,
                            "sport": resCompetition.data.competition.sport
                        };
                    })
                        .catch((error) => {
                        console.error(error)
                    })
                    promises.push(promise)
                }
                Promise.all(promises).then((_) => {
                    this.matches = matches
                });
            })
                .catch((error) => {
                console.error(error)
            });
        },
        disableAddMatch(match) {
            if (this.is_admin === 1) {
                return true
            }
            if (match.tickets_bought !== 0) {
                return true
            }
            if (this.money_available < match.price) {
                return true
            }
            return false
        },
        dissableAddTicket(match) {
            if (match.tickets_bought === match.total_available_tickets) {
                return true;
            }
            if (this.money_available < match.price) {
                return true
            }
            return false
        },
        addMatch() {
            const path = "https://a12-sportsmaster1.herokuapp.com/match/" + (this.matches.length+1)
            const parameters = {
              "local": this.addNewMatch.local,
              "visitor": this.addNewMatch.visitor,
              "date": this.addNewMatch.date,
              "price": this.addNewMatch.price,
              "competition": this.addNewMatch.competition,
              "total_available_tickets": this.addNewMatch.total_available_tickets
            }
            axios.post(path, parameters, { auth: {
                    username: this.token
                } })
                .then(() => {
                console.log("New match added")
                  this.getMatches();
            })
                .catch((error) => {
                // eslint-disable-next-line
                alert(error + " Your are not logged")
                console.log(error)
                this.getMatches()
            });
        },
        addPurchase(parameters) {
            const path = "https://a12-sportsmaster1.herokuapp.com/order/" + this.username
            axios.post(path, parameters, { auth: {
                    username: this.token
                } })
                .then(() => {
                console.log("Order done")
            })
                .catch((error) => {
                // eslint-disable-next-line
                alert(error + " Your are not logged")
                console.log(error)
                this.getMatches()
            });
        },
        addAllPurchases(orders) {
            const path = "https://a12-sportsmaster1.herokuapp.com/orders/" + this.username
            axios.post(path, { "orders": orders }, { auth: {
                    username: this.token
                } })
                .then(() => {
                console.log("Order done")
                this.restartToPurchase()
            })
                .catch((error) => {
                // eslint-disable-next-line
                alert(error + " Your are not logged")
                console.log(error);
                this.getMatches();
            });
        },
        deleteMatchFromBD(match){
          const pathMatch = "https://a12-sportsmaster1.herokuapp.com/match/" + match.id;
            axios.delete(pathMatch, { auth: {
                    username: this.token
                } })
                .then(() => {
                this.deleteMatch(match)
                console.log("Match deleted")
                this.restartToPurchase()
            })
                .catch((error) => {
                // eslint-disable-next-line
                alert(error + " Your are not logged")
                console.log(error);
                this.getMatches();
            });
        },
        restartToPurchase(){
          this.getMatches()
          this.getAccount()
          this.matches_added = []
          this.cistellaTotalMoney = 0
        },
        addOneTicket(match) {
            match.tickets_bought += 1;
            this.cistellaTotalMoney = Math.round((this.cistellaTotalMoney + match.price) * 100) / 100;
        },
        deleteOneTicket(match) {
            match.tickets_bought -= 1;
            this.cistellaTotalMoney = Math.round((this.cistellaTotalMoney - match.price) * 100) / 100;
            if (match.tickets_bought === 0) {
                this.matches_added = this.matches_added.filter((item) => item.id !== match.id)
            }
        },
        deleteMatch(match) {
            this.cistellaTotalMoney = Math.round((this.cistellaTotalMoney - match.price*match.tickets_bought) * 100) / 100;
            match.tickets_bought = 0;
            this.matches_added = this.matches_added.filter((item) => item.id !== match.id)
        },
        finalizePurchase() {
            var orders = [];
            for (let i = 0; i < this.matches_added.length; i += 1) {
                var order = {
                    match_id: this.matches_added[i].id,
                    tickets_bought: this.matches_added[i].tickets_bought
                };
                orders.push(order);
                // this.addPurchase(order)
                // this.matches_added[i].total_available_tickets -= this.matches_added[i].tickets_bought
                // this.matches_added[i].tickets_bought = 0
                // this.matches_added.splice(i)
            }
            this.addAllPurchases(orders);
        },
        checkFormValidity() {
        const valid = this.$refs.form.checkValidity()
        this.nameState = valid
        return valid
        },
        resetModal() {
          this.name = ''
          this.nameState = null
        },
        handleOk(bvModalEvent) {
          // Prevent modal from closing
          bvModalEvent.preventDefault()
          // Trigger submit handler
          this.handleSubmit()
        },
        handleSubmit() {
          // Exit when the form isn't valid
          if (!this.checkFormValidity()) {
            return
          }
          // Push the match to DB
          this.addMatch()
          // Hide the modal manually
          this.$nextTick(() => {
            this.$bvModal.hide('modal-prevent-closing')
          })
        }
    },
    created() {
      this.logged = this.$route.query.logged === "true";
      this.username = this.$route.query.username;
      this.token = this.$route.query.token;
      if (this.logged === true) {
          this.titleLogin = "LogOut"
          this.getAccount()
      }
      if (this.logged === undefined) {
          this.logged = false;
      }
      this.getMatches()
  }
}
</script>
