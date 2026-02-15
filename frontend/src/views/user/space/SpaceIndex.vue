<script setup>
import {useRoute,useRouter} from "vue-router";

const route = useRoute()

const router = useRouter()
</script>

<template>
个人空间：{{ route.params.user.id }}


</template>



<style scoped>

</style>