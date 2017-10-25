<?php 
$club = em()->getRepository('models\Club')->findOneById($notification->get_entity_id());
$user = NULL;
$is_ucroo = TRUE;
$user_id = $notification->get_user_from()->getId();
?>

<?php if (isset($is_menu)) { ?>
<div onclick="location.href='<?=base_url()?>club/<?=$club->getId()?>'">
<? } ?>

<?php
if(!empty($user_id)) {
  $user = get_user($user_id);
} else {
  return '<span class="msg_subtitle">Error: Member does\'t exist</span>';
}

$name = '';
if($is_ucroo && $user->getId() === get_userid())
  $name = 'You';
else if($is_ucroo)
  $name = anchor('user/profile/'.$user->getId(), get_name($user->getId()));
else 
  $name = $user->getFirst_name() . ' ' . $user->getLast_name();
?>

<?php 
$iconClass = 'post-icon';
$detailsClass = 'post-details';
if (isset($is_menu)) { 
  $iconClass = 'msg-icon';
  $detailsClass = 'msg-details';
}
?>

<div class="<?=$iconClass?>">
  <a href="<?=base_url()?>user/profile/<?=$user_id?>"><img src="<?=get_user_profile_pic($user_id, 'square') ?>" alt='User Profile'/></a>
</div>

<div class="<?=$detailsClass?>">
  <?php if (!isset($is_menu)) { ?>
  <div class="float-right icon-delete"><a href="<?=base_url()?>notification/delete/<?=$notification->get_id()?>" title="delete"><div class="only-web-hidden">Delete</div></a></div>
  <? } ?>
  	<img style="height: 33px; float: left; padding-right: 8px" src="<?=get_club_picture_thumb($club)?>">
	<?php if($is_ucroo):?>
	  <span class="user-name"><?= anchor('user/profile/'.$user->getId().prepare_que_str_mobile('UserInfo',$user->getId()), $name) ?></span>
	<?php else:?>
	  <span class="user-name"><?=$name?></span>
	<?php endif;?>
	 invited you to join <?= anchor('club/'.$club->getId().prepare_que_str_mobile($notification).prepare_que_str_mobile($notification), $club->getName() . ' (' . $club->getShort_name() . ')')?>
</div>
