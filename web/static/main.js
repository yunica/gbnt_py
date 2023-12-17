const APIS = ["employees_by_departments_jobs_quarter", "employees_hired_by_department"]
const App = {
    delimiters: ['[[', ']]'],
    components: {
        EasyDataTable: window['vue3-easy-data-table'],
    },
    data() {
        return {
            employees_by_departments_jobs_quarter: {
                headers: [
                    {text: "PLAYER", value: "departments", sortable: true},
                    {text: "TEAM", value: "jobs", sortable: true},
                    {text: "Q1", value: "Q1"},
                    {text: "Q2", value: "Q2"},
                    {text: "Q3", value: "Q3"},
                    {text: "Q4", value: "Q4"},
                ],
                items: []
            },
            employees_hired_by_department: {
                headers: [
                    {text: "ID", value: "department__id"},
                    {text: "DEPARTMENT", value: "department__department"},
                    {text: "HIRED", value: "hired", sortable: true},
                ],
                items: []
            },
            year: 2021,
            message: 'Hello Vue!',
        }
    },

    methods: {
        fetch_data(year_) {
            if (!year_) {
                year_ = this.year
            }
            APIS.forEach(async i => {
                this[i].items = []
                await axios.get(`/api/${i}`, {params: {year: year_}}).then(resp => {
                    this[i].items = [...resp.data]
                }).catch(err => console.error(err));
            })

        }
    },
    mounted() {
        this.fetch_data()
    },
    watch: {
        year(newYear, oldYear) {
            console.log(newYear, oldYear)
            if (newYear !== oldYear) {
                this.fetch_data(newYear)
            }
        }
    },
};

Vue.createApp(App).mount("#app");