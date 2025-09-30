<template>
  <div class="case-studies-page">
    <h2>Case Studies</h2>
    <div class="flex-box">
      <div>
        <h3>Milton: Sidewalk Gap Project</h3>
        <p>Since 2016, the Town of Milton has expanded its pedestrian system so there is now 7.25 miles of interconnected sidewalk. The town did this by building connections between pre-existing segments and creating new sidewalks at key points in the community, including through residential areas, and to Husky Technologies, a major employer.</p>
        <p>In Milton improving walkability is closely linked with downtown revitalization efforts. The town’s process in realizing these efforts might also be useful as a case study because officials took different approaches to funding various segments, including state and federal grants, town funds, and private partnerships.</p>
      </div>
      <img src="https://via.placeholder.com/400" class="img-placeholder" alt="Milton Sidewalks" style="max-width: 400px; margin-left: 20px;" />
    </div>
    <hr></hr>
    <div class="flex-box">
      <div>
        <h3>South Burlington: Penny for Paths</h3>
        <p>South Burlington adopted an innovative approach to raising funds for bike and pedestrian projects: residents voted in 2018 to implement a 1 cent increase on the tax rate. The city’s Bicycle and Pedestrian Committee recommends projects to prioritize, often aimed at closing gaps between existing sidewalk and paths.</p>
        <p>So far, the fund has supported projects including extension of a shared-use path at Allen Road and Spear Street, new crosswalks on Williston Road, and flashing beacons at crossings on Patchen Road. The city is working on closing a 3,500-foot gap in the Spear Street multi-use path, which will open an important connection between South Burlington and downtown Burlington. Coming up with funding for single-occupancy vehicle alternative projects is a common hurdle, and this model can be informative for other municipalities.</p>
      </div>
      <img src="https://via.placeholder.com/400" class="img-placeholder" alt="Milton Sidewalks" style="max-width: 400px; margin-left: 20px;" />
    </div>
    <hr></hr>
    <div class="flex-box">
      <div>
        <h3>Work = Play: Commuting by rec trail</h3>
        <p>Networks of separated multi-use trails are expanding across Vermont. Trail systems like the Lamoille Valley Rail Trail and the Cross Vermont Trail often appear in media as recreational attractions. However, these trail networks are also attractive corridors for bike commuting away from vehicle traffic , particularly as communities build out points of connection with trails, as in Hardwick and Johnson.</p>
        <p>Many new segments of trails offer dual functional and recreational use. To point to a couple: .</p>
        <ul>
          <li>Newport: The trail expansion between Prouty Beach and Bluffside Farm, including a new bridge over Scott’s Cove, not only connected downtown with recreation, it also opened a key connection for bike commuters to North Country Hospital. This and other efforts earned the health center a <a href="https://bikeleague.org/wp-content/uploads/2024/05/BFB_Full_List_through_Spring-2024-1.pdf">Silver Bicycle Friendly Business Award</a> from the League of American Bicyclists.</li>
          <li>East Montpelier: The Cross Vermont Trail is completing a <a href="https://www.crossvermont.org/about_us/gallery_newscroll.htm">connector trail to U-32 Middle & High School</a>, building on the installation of a key bridge over the Winooski River in 2021. That bridge helps connect Montpelier, East Montpelier and Berlin.</li>
        </ul>
      </div>
      <img src="https://via.placeholder.com/400" class="img-placeholder" alt="Milton Sidewalks" style="max-width: 400px; margin-left: 20px;" />
    </div>
    <hr></hr>
    <div class="flex-box">
      <div>
        <h3>Waitsfield</h3>
        <p>After a pedestrian fatality in 2020, the town began a concerted effort to improve safety along Route 100, the state-owned highway that also serves as Waitsfield’s Main Street.</p>
        <p>Working collaboratively with concerned community members, local planning groups, a state representative and a team from the Vermont Agency of Transportation, the town identified key challenges for pedestrian safety, and began working on short- and long-term solutions. As a result of this coordinated effort, many changes have been implemented along Route 100, including new crosswalks, bump-outs, and rapid flashing beacons. A new MRV Recreation Hub and Welcome Center was completed in 2024, which directs bike and pedestrian traffic to an alternative path for part of the town. The town is continuing to expand on the infrastructure already implemented, and has an ongoing process tracking the status of efforts to address safety concerns.</p>
      </div>
      <img src="https://via.placeholder.com/400" class="img-placeholder" alt="Milton Sidewalks" style="max-width: 400px; margin-left: 20px;" />
    </div>
    <!-- <SimpleAccordion :items="caseStudies" /> -->
  </div>
</template>

<script setup>
import SimpleAccordion from '../components/SimpleAccordion.vue';

const caseStudies = [
  {
    label: 'Burlington Greenway Extension',
    content: `The Burlington Greenway Extension project connected the city's popular multi-use path to new neighborhoods, increasing access for both commuters and recreational users. The project included new signage, improved crossings, and community engagement to ensure the path met local needs.`
  },
  {
    label: 'Montpelier Microtransit Pilot',
    content: `Montpelier launched a microtransit pilot in 2023, providing on-demand rides for residents without access to fixed-route transit. The pilot reduced single-occupancy vehicle trips and provided valuable data for future transit planning.`
  },
  {
    label: 'Brattleboro E-Bike Library',
    content: `Brattleboro's E-Bike Library program allowed residents to borrow e-bikes for up to two weeks, encouraging active transportation and reducing car dependency. The program was supported by local businesses and received positive feedback from participants.`
  }
];
</script>

<style scoped>

p, h2, h3 {
  padding: 12px
}
.case-studies-page {
  max-width: 1000px;
}

.flex-box {
  display: flex;
}

.flex-box * {
  flex: 1;
}

hr {
  margin-top: 10px;
  margin-bottom: 10px;
}

@media (max-width: 800px) {
  .flex-box {
    flex-direction: column-reverse;
  }
  .flex-box img {
    margin-left: 0 !important;
    margin-top: 20px;
    max-width: 100% !important;
  }
}
</style>
