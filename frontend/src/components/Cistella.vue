<template>
  <div>
    <div class="container">
      <header class="d-flex flex-wrap justify-content-between py-3 mb-4 border-bottom">
        <h1 class="fs-4 mb-3 mb-md-0 me-md-auto"> {{ title }} </h1>
        <button class="btn btn-primary btn-lg" :disabled="money_available < price_match" @click="closePage">Tanca Cistella</button>
      </header>
    </div>
    <div class="container">
    <div class="col-lg-12 grid-margin stretch-card">
      <div style="margin-left:auto;margin-right:auto;" class="card">
        <div class="card-body">
          <h4 class="card-title">Cart</h4>
          <div class="table-responsive">
            <table v-if="isShow" style="margin-left:auto;margin-right:auto;" class="table">
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
                <tr v-for="(match) in matches" :key="match.id">
                  <th scope="row">{{ match.competition.sport  }}</th>
                  <td>{{ match.competition.name}}</td>
                  <td><strong>{{ match.local.name }}</strong> ({{ match.local.country }}) vs <strong>{{ match.visitor.name }}</strong> ({{ match.visitor.country }})</td>
                  <td>
                    {{ match.tickets_bought}}
                    <button class="badge badge-danger" @click="deleteOneTicket(match)">-</button>
                    <button class="badge badge-success" @click="addOneTicket(match)">+</button>
                  </td>
                  <td>{{ match.price}} &euro;</td>
                  <th>
                    <button class="badge badge-danger" @click="deleteMatch(match.id)">Eliminar entrada</button>
                  </th>
                </tr>
              </tbody>
            </table>
            <h6 v-if="!isShow" class="card-title">Your cart is currently empty</h6>
          </div>
          <button class="btn btn-secondary">Enrere</button>
          <button @click="finalizePurchase" class="btn btn-success">Finalitzar la compra</button>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios'

export default {
  data () {
    return {
      title: 'Sport Matches',
      tickets_bought: 0,
      money_available: 20.0,
      price_match: 10.0,
      isShow: true,
      orders: [
        {
          'match_id': 1,
          'tickets_bought': 1
        }
      ],
      matches: [
        {
          'id': 1,
          'local': {
            'id': 3,
            'name': 'Club Juventut Les Corts',
            'country': 'Spain'
          },
          'visitor': {
            'id': 2,
            'name': 'CE Sabadell',
            'country': 'Spain'
          },
          'competition': {
            'name': 'Women\'s European Championship',
            'category': 'Senior',
            'sport': 'Volleyball'
          },
          'date': '2022-10-12T00:00:00',
          'price': 4.3,
          'tickets_bought': 7
        },
        {
          'id': 2,
          'local': {
            'id': 3,
            'name': 'Club Juventut Les Corts',
            'country': 'Spain'
          },
          'visitor': {
            'id': 2,
            'name': 'CE Sabadell',
            'country': 'Spain'
          },
          'competition': {
            'name': '1st Division League',
            'category': 'Junior',
            'sport': 'Football'
          },
          'date': '2022-07-10T00:00:00',
          'price': 129.29,
          'tickets_bought': 3
        },
        {
          'id': 3,
          'local': {
            'id': 1,
            'name': 'CV Vall D\'Hebron',
            'country': 'Spain'
          },
          'visitor': {
            'id': 4,
            'name': 'Volei Rubi',
            'country': 'Spain'
          },
          'competition': {
            'name': '1st Division League',
            'category': 'Junior',
            'sport': 'Football'
          },
          'date': '2022-08-10T00:00:00',
          'price': 111.1,
          'tickets_bought': 2
        }
      ],
      matches_added: [{
        'id': 3,
        'local': {
          'id': 1,
          'name': 'CV Vall D\'Hebron',
          'country': 'Spain'
        },
        'visitor': {
          'id': 4,
          'name': 'Volei Rubi',
          'country': 'Spain'
        },
        'competition': {
          'name': '1st Division League',
          'category': 'Junior',
          'sport': 'Football'
        },
        'date': '2022-08-10T00:00:00',
        'price': 111.1,
        'tickets_bought': 2
      }]
    }
  },
  methods: {
    closePage () {
      this.$router.replace({path: '/'})
    },
    addOneTicket (match) {
      match.tickets_bought += 1
    },
    deleteOneTicket (match) {
      match.tickets_bought -= 1
    },
    deleteMatch (id) {
      this.matches.splice(id - 1, 1)
    },
    addPurchase (parameters) {
      const path = 'https://a12-sportsmaster1.herokuapp.com/order/test'
      axios.post(path, parameters)
        .then(() => {
          console.log('Order done')
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.getMatches()
        })
    },
    finalizePurchase () {
      this.isShow = !this.isShow
      for (let i = 0; i < this.matches_added.length; i += 1) {
        const parameters = {
          match_id: this.matches_added[i].id,
          tickets_bought: this.matches_added[i].tickets_bought
        }
        this.addPurchase(parameters)
      }
      this.matches_added.splice(0)
    },
    getMatches () {
      const pathMatches = 'https://a12-sportsmaster1.herokuapp.com/matches'
      const pathCompetition = 'https://a12-sportsmaster1.herokuapp.com/competition/'

      axios.get(pathMatches)
        .then((res) => {
          var matches = res.data.matches.filter((order) => {
            return order.competition_id != null
          })
          var promises = []
          for (let i = 0; i < matches.length; i++) {
            const promise = axios.get(pathCompetition + matches[i].competition_id)
              .then((resCompetition) => {
                delete matches[i].competition_id
                matches[i].competition = {
                  'name': resCompetition.data.competition.name,
                  'category': resCompetition.data.competition.category,
                  'sport': resCompetition.data.competition.sport
                }
              })
              .catch((error) => {
                console.error(error)
              })
            promises.push(promise)
          }
          Promise.all(promises).then((_) => {
            this.matches = matches
          })
        })
        .catch((error) => {
          console.error(error)
        })
    }
  },
  created () {
    this.getMatches()
  }
}

</script>
